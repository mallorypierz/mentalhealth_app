"""Live adapter contracts with synthetic WAV and intercepted HTTP; never paid calls."""
import asyncio
import base64
import io
import wave
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch, AsyncMock
import httpx
from dataclasses import replace
from backend.app.config import Settings,load
from backend.app.db import initialize,connect
from backend.app.providers.live_voice import AudioProvider,VoiceFailure,validate_wav
from backend.app.repositories import voice_budget
from backend.app.repositories.provider_usage import LimitError
from backend.tests import test_voice as base
uid=base.uid
from fastapi.testclient import TestClient
from backend.app.main import create_app

def wav():
    out=io.BytesIO()
    with wave.open(out,'wb') as w:
        w.setnchannels(1);w.setsampwidth(2);w.setframerate(16000);w.writeframes(b'\0\0'*4000)
    return out.getvalue()

class AdapterTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.path=Path(self.tmp.name)/'test.sqlite3';initialize(self.path,True)
        self.settings=Settings(provider='openai',api_key='test-only',voice_enabled=True,voice_prices_verified=True,voice_call_limit=20,voice_budget_microdollars=1000000,voice_test_session_id='11111111-1111-4111-8111-111111111111')
        voice_budget.create_test_session(self.path,self.settings.voice_test_session_id,'Mock test',50,2500000)
    def tearDown(self): self.tmp.cleanup()
    def test_disabled_never_calls_transport(self):
        provider=AudioProvider(self.path,Settings(),httpx.MockTransport(lambda r: self.fail('Network must not run')))
        with self.assertRaises(VoiceFailure): asyncio.run(provider.transcribe(wav(),'a'))
        with connect(self.path) as db: self.assertEqual(db.execute('SELECT COUNT(*) FROM voice_provider_attempts').fetchone()[0],0)
    def test_transcription_speech_and_duplicate_cost(self):
        calls=[]
        def handler(r):
            calls.append(r.url.path)
            return httpx.Response(200,json={'text':'Fictional question'}) if r.url.path.endswith('transcriptions') else httpx.Response(200,content=b'\x01\x00'*2400)
        provider=AudioProvider(self.path,self.settings,httpx.MockTransport(handler))
        self.assertEqual(asyncio.run(provider.transcribe(wav(),'a')),'Fictional question')
        spoken=asyncio.run(provider.speak('A reviewed reply.','b'))
        with wave.open(io.BytesIO(spoken)) as output:
            self.assertEqual(output.getframerate(),24000);self.assertEqual(output.getnframes(),2400)
        with self.assertRaises(VoiceFailure): asyncio.run(provider.transcribe(wav(),'a'))
        self.assertEqual(len(calls),2)
    def test_pcm_wrapping_exact_length_and_invalid_samples(self):
        from backend.app.providers.live_voice import pcm_to_wav
        for raw in [b'',b'x',b'xx'*2000001]:
            with self.assertRaises(VoiceFailure):pcm_to_wav(raw)
        raw=b'\x01\x00'*24000
        with wave.open(io.BytesIO(pcm_to_wav(raw))) as result:
            self.assertEqual(result.getnframes(),24000)
            self.assertEqual(result.readframes(result.getnframes()),raw)

    def test_failures_count_and_budget_survives_reopen(self):
        provider=AudioProvider(self.path,self.settings,httpx.MockTransport(lambda r:httpx.Response(401)))
        for i in range(20):
            with self.assertRaisesRegex(VoiceFailure,'provider_http_401'): asyncio.run(provider.transcribe(wav(),str(i)))
        initialize(self.path,True)
        with self.assertRaisesRegex(VoiceFailure,'budget_exhausted'): asyncio.run(provider.transcribe(wav(),'new'))
        with connect(self.path) as db:
            self.assertEqual(tuple(db.execute('SELECT COUNT(*),SUM(reserved_microdollars) FROM voice_provider_attempts').fetchone()),(20,1000000))
    def test_approved_extension_keeps_previous_usage(self):
        previous=replace(self.settings,voice_call_limit=25,voice_budget_microdollars=1250000)
        for i in range(25): voice_budget.reserve(self.path,str(i),'speech',previous)
        extended=replace(self.settings,voice_call_limit=50,voice_budget_microdollars=2500000)
        for i in range(25,50): voice_budget.reserve(self.path,str(i),'speech',extended)
        with self.assertRaisesRegex(LimitError,'budget_exhausted'):
            voice_budget.reserve(self.path,'extra','speech',extended)
        with connect(self.path) as db:
            self.assertEqual(tuple(db.execute('SELECT COUNT(*),SUM(reserved_microdollars) FROM voice_provider_attempts').fetchone()),(50,2500000))
        with self.assertRaises(ValueError):
            replace(extended,voice_call_limit=51).require_voice()

    def test_malformed_audio_and_response(self):
        for value in [b'not audio',wav()[:-2]]:
            with self.assertRaises(VoiceFailure): validate_wav(value)
        provider=AudioProvider(self.path,self.settings,httpx.MockTransport(lambda r:httpx.Response(200,json={'text':''})))
        with self.assertRaisesRegex(VoiceFailure,'invalid_transcription'): asyncio.run(provider.transcribe(wav(),'bad'))
    def test_concurrent_reservations_cannot_exceed_cap(self):
        from concurrent.futures import ThreadPoolExecutor
        def attempt(i):
            try: voice_budget.reserve(self.path,str(i),'transcription',self.settings);return 1
            except LimitError:return 0
        with ThreadPoolExecutor(max_workers=8) as pool: self.assertEqual(sum(pool.map(attempt,range(30))),20)

class LiveRoundTrip(base.VoiceTests):
    # Reuse identity/socket helpers; inherited mock tests are not appropriate here.
    def setUp(self):
        super().setUp()
        self.client.__exit__(None,None,None)
        self.settings=Settings(provider='openai',api_key='test-only',voice_enabled=True,voice_prices_verified=True,voice_call_limit=20,voice_budget_microdollars=1000000,voice_test_session_id='11111111-1111-4111-8111-111111111111')
        voice_budget.create_test_session(self.path,self.settings.voice_test_session_id,'Mock test',50,2500000)
        self.client=TestClient(create_app(self.path,settings=self.settings,enable_profiles=True));self.client.__enter__()
        self.body={'session_id':uid(),'conversation_id':self.conv,'operation_id':uid()}
        self.session=self.client.post('/api/voice/sessions',headers=self.headers,json=self.body).json()
    def test_real_audio_contract_with_intercepted_providers(self):
        from backend.app.providers.openai import Provider
        from backend.app.providers import mock
        async def plan(instance,q,s,m):
            instance.ledger.reserve(instance.path,instance.request_id,'planning',instance.settings)
            return await mock.plan(q,s,m)
        async def answer(instance,q,c,s,m):
            instance.ledger.reserve(instance.path,instance.request_id,'answer',instance.settings)
            return {'content':'There are no matching saved records.','citations':[]}
        async def transcribe(instance,data,key):
            validate_wav(data);voice_budget.reserve(instance.path,key,'transcription',instance.settings)
            return 'Fictional: what happened in my last breathing practice?'
        async def speak(instance,text,key):
            voice_budget.reserve(instance.path,key,'speech',instance.settings);return wav()
        with patch.object(AudioProvider,'transcribe',transcribe),patch.object(AudioProvider,'speak',speak),patch.object(Provider,'plan',plan),patch.object(Provider,'answer',answer):
            with self.socket() as ws:
                self.authenticate(ws)
                body={'type':'audio_turn','turn_id':uid(),'request_id':uid(),'operation_id':uid(),'audio':base64.b64encode(wav()).decode()}
                ws.send_json(body); result=self.finish()
                self.assertEqual(result['request']['assistant_persistence'],'saved',result)
                self.assertEqual(result['provider'],'openai')
                self.assertEqual(result['speech'],'ready')
                ws.send_json(body)
                self.assertEqual(self.client.get('/api/voice/turns/'+body['turn_id']+'/audio',headers=self.headers).content,wav())
                with connect(self.path) as db:
                    self.assertEqual(db.execute('SELECT COUNT(*) FROM messages').fetchone()[0],2)
                    self.assertEqual(db.execute('SELECT COUNT(*) FROM voice_provider_attempts').fetchone()[0],4)
                    self.assertEqual(db.execute('PRAGMA foreign_key_check').fetchall(),[])
# Only execute the new live contract in this subclass; the original suite is separate.
for name in dir(base.VoiceTests):
    if name.startswith('test_'): setattr(LiveRoundTrip,name,None)
