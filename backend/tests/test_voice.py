import tempfile
import time
import unittest
from pathlib import Path
from uuid import uuid4
from fastapi.testclient import TestClient
from backend.app.main import create_app
from backend.app.db import connect


def uid(): return str(uuid4())

class VoiceTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory(); self.path=Path(self.tmp.name)/'voice.sqlite3'
        self.client=TestClient(create_app(self.path,enable_profiles=True)); self.client.__enter__()
        self.headers=self.identity()
        self.conv=uid()
        self.client.post('/api/conversations',headers=self.headers,json={'conversation_id':self.conv,'operation_id':uid()})
        self.body={'session_id':uid(),'conversation_id':self.conv,'operation_id':uid()}
        response=self.client.post('/api/voice/sessions',headers=self.headers,json=self.body)
        self.assertEqual(response.status_code,201,response.text)
        self.session=response.json()

    def tearDown(self):
        self.client.__exit__(None,None,None); self.tmp.cleanup()

    def identity(self, name=None):
        data=self.client.post('/api/identity/bootstrap',json={'bootstrap_id':uid()}).json()
        headers={'Authorization':'Bearer '+data['access_token']}
        if name:
            profile=uid()
            self.client.post('/api/profiles',headers=headers,json={'profile_id':profile,'operation_id':uid(),'display_name':name})
            self.client.post('/api/identity/select',headers=headers,json={'profile_id':profile,'operation_id':uid(),'expected_context_version':1})
        else:
            self.client.post('/api/identity/guest',headers=headers,json={'operation_id':uid(),'expected_context_version':1})
        headers['X-Context-Version']='2'
        return headers

    def socket(self, headers=None):
        return self.client.websocket_connect('/api/voice/stream',headers={'Origin':'http://127.0.0.1:5173'})

    def authenticate(self,ws,headers=None):
        headers=headers or self.headers
        ws.send_json({'type':'authenticate','token':headers['Authorization'][7:],'context_version':2,'session_id':self.session['id']})
        self.assertEqual(ws.receive_json()['type'],'ready')

    def turn(self,scenario='success'):
        return {'type':'mock_turn','turn_id':uid(),'request_id':uid(),'operation_id':uid(),'scenario':scenario}

    def state(self):
        response=self.client.get('/api/voice/sessions/'+self.session['id'],headers=self.headers)
        self.assertEqual(response.status_code,200,response.text)
        return response.json()

    def finish(self):
        for _ in range(150):
            state=self.state()
            if state['turns'] and state['turns'][-1]['state']!='processing': return state['turns'][-1]
            time.sleep(.02)
        self.fail('turn remained processing')

    def test_save_read_duplicate_success_order_audio_restart(self):
        self.assertEqual(self.client.post('/api/voice/sessions',headers=self.headers,json=self.body).status_code,200)
        with self.socket() as ws:
            self.authenticate(ws); body=self.turn(); ws.send_json(body); ws.send_json(body)
            result=self.finish()
            self.assertEqual(result['state'],'completed')
            self.assertEqual(result['submission'],'saved'); self.assertEqual(result['speech'],'ready')
            audio=self.client.get('/api/voice/turns/'+body['turn_id']+'/audio',headers=self.headers)
            self.assertEqual(audio.status_code,200); self.assertTrue(audio.content.startswith(b'RIFF'))
            rows=self.client.get('/api/conversations/'+self.conv+'/messages',headers=self.headers).json()['messages']
            self.assertEqual([r['sequence'] for r in rows],[1,2]); self.assertEqual([r['role'] for r in rows],['user','assistant'])
            with connect(self.path) as db:
                self.assertEqual(db.execute('SELECT count(*) FROM voice_turns').fetchone()[0],1)
                self.assertEqual(db.execute('SELECT content FROM messages WHERE role="assistant"').fetchone()[0],result['request']['assistant_content'])
                self.assertEqual(db.execute('SELECT count(*) FROM provider_attempts').fetchone()[0],0)
            second=self.turn(); ws.send_json(second); self.finish()
            self.assertEqual([t['sequence'] for t in self.state()['turns']],[1,2])
        with TestClient(create_app(self.path,enable_profiles=True)) as restart:
            after=restart.get('/api/voice/sessions/'+self.session['id'],headers=self.headers).json()
            self.assertEqual(len(after['turns']),2)
            self.assertNotIn(after['state'],['active','ready'])
            self.assertEqual(restart.get('/api/voice/turns/'+body['turn_id']+'/audio',headers=self.headers).status_code,410)

    def test_stage_failures_no_fabricated_assistant(self):
        with self.socket() as ws:
            self.authenticate(ws)
            for scenario in ['transcription_failure','model_failure','speech_failure']:
                before=len(self.state()['turns']); ws.send_json(self.turn(scenario))
                for _ in range(100):
                    if len(self.state()['turns'])>before: break
                    time.sleep(.01)
                result=self.finish()
                if scenario=='transcription_failure':
                    self.assertIsNone(result['request']); self.assertEqual(result['transcription'],'failed')
                elif scenario=='model_failure':
                    self.assertEqual(result['request']['assistant_persistence'],'not_saved')
                    self.assertEqual(result['request']['status'],'failed')
                else:
                    self.assertEqual(result['speech'],'failed')
                    self.assertEqual(result['request']['assistant_persistence'],'saved')
                    action={'operation_id':uid(),'expected_revision':result['revision'],'action':'retry_speech'}
                    response=self.client.post('/api/voice/turns/'+result['id']+'/actions',headers=self.headers,json=action)
                    self.assertEqual(response.status_code,200,response.text)
                    self.assertEqual(response.json()['speech'],'ready')
                    self.assertEqual(self.client.post('/api/voice/turns/'+result['id']+'/actions',headers=self.headers,json=action).status_code,200)

    def test_cancel_prevents_late_submission_and_switch_requires_stop(self):
        with self.socket() as ws:
            self.authenticate(ws); ws.send_json(self.turn('delayed'))
            ws.receive_json()
            turn=self.state()['turns'][0]
            url='/api/voice/turns/'+turn['id']+'/actions'
            body={'operation_id':uid(),'expected_revision':turn['revision'],'action':'cancel'}
            self.assertEqual(self.client.post(url,headers=self.headers,json=body).status_code,200)
            self.assertEqual(self.client.post(url,headers=self.headers,json=body).status_code,200)
            time.sleep(2.1)
            self.assertEqual(self.state()['turns'][0]['state'],'cancelled')
            with connect(self.path) as db: self.assertEqual(db.execute('SELECT count(*) FROM messages').fetchone()[0],0)
            result=self.client.post('/api/identity/leave',headers=self.headers,json={'operation_id':uid(),'expected_context_version':2,'confirm_discard':True})
            self.assertEqual(result.status_code,409)
        result=self.client.post('/api/identity/leave',headers=self.headers,json={'operation_id':uid(),'expected_context_version':2,'confirm_discard':True})
        self.assertEqual(result.status_code,200,result.text)

    def test_profile_isolation_and_stale_context(self):
        for name in ['Fictional A','Fictional B']:
            other=self.identity(name)
            self.assertEqual(self.client.get('/api/voice/sessions/'+self.session['id'],headers=other).status_code,404)
            with self.socket() as ws:
                ws.send_json({'type':'authenticate','token':other['Authorization'][7:],'context_version':2,'session_id':self.session['id']})
                self.assertEqual(ws.receive_json()['type'],'error')
        stale=self.headers|{'X-Context-Version':'1'}
        self.assertEqual(self.client.get('/api/voice/sessions/'+self.session['id'],headers=stale).status_code,409)
        with self.socket() as ws:
            self.authenticate(ws)
            with connect(self.path) as db: db.execute('UPDATE browser_sessions SET context_version=context_version+1')
            ws.send_json(self.turn())
            self.assertEqual(ws.receive_json()['code'],'stale_context')
        with connect(self.path) as db: self.assertEqual(db.execute('SELECT count(*) FROM messages').fetchone()[0],0)

    def test_user_and_reply_save_failures(self):
        for role in ['user','assistant']:
            with connect(self.path) as db:
                db.execute("CREATE TRIGGER reject_message BEFORE INSERT ON messages WHEN NEW.role='"+role+"' BEGIN SELECT RAISE(ABORT,'test failure'); END")
            with self.socket() as ws:
                self.authenticate(ws); ws.send_json(self.turn()); result=self.finish()
                self.assertEqual(result['state'],'failed')
                self.assertEqual(result['error_code'],'transcript_save_failed' if role=='user' else 'reply_save_failed')
                with connect(self.path) as db:
                    self.assertEqual(db.execute("SELECT count(*) FROM messages WHERE role='assistant'").fetchone()[0],0)
            with connect(self.path) as db: db.execute('DROP TRIGGER reject_message')
            self.body={'session_id':uid(),'conversation_id':self.conv,'operation_id':uid()}
            self.session=self.client.post('/api/voice/sessions',headers=self.headers,json=self.body).json()

    def test_retry_reply_save_uses_retained_text_without_new_generation(self):
        with connect(self.path) as db:
            db.execute("CREATE TRIGGER reject_reply BEFORE INSERT ON messages WHEN NEW.role='assistant' BEGIN SELECT RAISE(ABORT,'test'); END")
        with self.socket() as ws:
            self.authenticate(ws); ws.send_json(self.turn()); result=self.finish()
            self.assertEqual(result['error_code'],'reply_save_failed')
            with connect(self.path) as db: db.execute('DROP TRIGGER reject_reply')
            body={'operation_id':uid(),'expected_revision':result['revision'],'action':'retry_reply_save'}
            url='/api/voice/turns/'+result['id']+'/actions'
            response=self.client.post(url,headers=self.headers,json=body)
            self.assertEqual(response.status_code,200,response.text)
            saved=response.json()
            self.assertEqual(saved['request']['status'],'succeeded')
            self.assertEqual(saved['request']['provider_call_count'],2)
            self.assertEqual(saved['request']['assistant_persistence'],'saved')
            self.assertEqual(self.client.post(url,headers=self.headers,json=body).status_code,200)
            with connect(self.path) as db:
                self.assertEqual(db.execute('SELECT count(*) FROM messages').fetchone()[0],2)

    def test_voice_rag_retrieves_only_active_guest_among_two_profiles(self):
        expected=None
        for headers in [self.identity('Fictional A'),self.identity('Fictional B'),self.headers]:
            ident=uid()
            result=self.client.post('/api/sessions',headers=headers,json={'session_id':ident,'operation_id':uid(),
                'skill_key':'paced_breathing_4_6','started_at':'2026-10-26T12:00:00Z'})
            self.assertEqual(result.status_code,201,result.text)
            if headers is self.headers: expected=ident
        with self.socket() as ws:
            self.authenticate(ws); ws.send_json(self.turn()); result=self.finish()
            self.assertEqual(result['request']['retrieved_record_ids'],[expected])
            self.assertEqual(result['request']['citations'],[expected])
            self.assertEqual(result['request']['retrieval_outcome'],'records')
            with connect(self.path) as db:
                self.assertEqual(db.execute('PRAGMA foreign_key_check').fetchall(),[])

    def test_conflicting_replay_and_socket_origin_rejected(self):
        with self.socket() as ws:
            self.authenticate(ws); body=self.turn(); ws.send_json(body); self.finish()
            ws.send_json(body|{'scenario':'model_failure'})
            events=[]
            while True:
                event=ws.receive_json(); events.append(event)
                if event['type']=='error': break
            self.assertEqual(events[-1]['code'],'voice_connection_failed')
        with connect(self.path) as db:
            self.assertEqual(db.execute('SELECT count(*) FROM voice_turns').fetchone()[0],1)
            self.assertEqual(db.execute('SELECT count(*) FROM messages').fetchone()[0],2)
        from starlette.websockets import WebSocketDisconnect
        with self.assertRaises(WebSocketDisconnect):
            with self.client.websocket_connect('/api/voice/stream',headers={'Origin':'https://unrelated.example'}): pass

    def test_crisis_transcript_held_before_history_or_rag_without_logging_words(self):
        from unittest.mock import patch, AsyncMock
        from backend.app.providers import voice as fixtures, mock
        with patch.object(fixtures,'transcribe',AsyncMock(return_value='Fictional: I might do something to myself')), \
             patch.object(mock,'plan',AsyncMock(side_effect=AssertionError('No model planning allowed'))), \
             patch.object(fixtures,'speak',AsyncMock(side_effect=AssertionError('No audio allowed'))):
            with self.socket() as ws:
                self.authenticate(ws); ws.send_json(self.turn())
                event=ws.receive_json()
                self.assertEqual(event['type'],'accepted')
                event=ws.receive_json()
                self.assertEqual(event['type'],'support_notice')
                self.assertEqual(event['submission'],'not_saved')
                state=self.state()
                self.assertEqual(state['state'],'stopped')
                self.assertEqual(state['turns'][0]['state'],'held')
                self.assertIsNone(state['turns'][0]['request'])
                with connect(self.path) as db:
                    self.assertEqual(db.execute('SELECT count(*) FROM messages').fetchone()[0],0)
                    self.assertEqual(db.execute('SELECT count(*) FROM requests').fetchone()[0],0)
                    self.assertNotIn('something to myself',str([tuple(r) for r in db.execute('SELECT * FROM voice_turns')]))

    def test_unsafe_generated_voice_reply_not_saved_or_spoken(self):
        from unittest.mock import patch, AsyncMock
        from backend.app.providers import voice as fixtures, mock
        with patch.object(mock,'answer',AsyncMock(return_value={'content':'Everything will be fine.','citations':[]})), \
             patch.object(fixtures,'speak',AsyncMock(side_effect=AssertionError('No audio allowed'))):
            with self.socket() as ws:
                self.authenticate(ws); ws.send_json(self.turn()); result=self.finish()
                self.assertEqual(result['error_code'],'response_unavailable')
                self.assertEqual(result['request']['assistant_persistence'],'not_saved')
                self.assertEqual(result['speech'],'not_started')
                self.assertEqual(result['request']['user_persistence'],'saved')

    def test_latest_voice_controls_restore_without_calls_and_enforce_owner(self):
        url='/api/voice/conversations/'+self.conv+'/latest-turn'
        self.assertIsNone(self.client.get(url,headers=self.headers).json()['turn'])
        with self.socket() as ws:
            self.authenticate(ws);ws.send_json(self.turn());result=self.finish()
        restored=self.client.get(url,headers=self.headers)
        self.assertEqual(restored.status_code,200)
        self.assertEqual(restored.json()['turn']['id'],result['id'])
        other=self.identity('Fictional other owner')
        self.assertEqual(self.client.get(url,headers=other).status_code,404)
        with connect(self.path) as db:
            self.assertEqual(db.execute('SELECT COUNT(*) FROM messages').fetchone()[0],2)
            self.assertEqual(db.execute('SELECT COUNT(*) FROM voice_provider_attempts').fetchone()[0],0)
