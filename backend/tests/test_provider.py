import asyncio
import json
import tempfile
import unittest
from pathlib import Path
from uuid import uuid4
import httpx
from fastapi.testclient import TestClient
from backend.app.config import Settings, load, MODEL
from backend.app.db import initialize, connect
from backend.app.providers.openai import Provider, PLAN
from backend.app.rag.pipeline import RAGFailure
from backend.app.repositories import provider_usage as usage, conversations as records
from backend.app.chat_schemas import ConversationCreate, MessageSubmit
from backend.app.main import create_app

class ProviderTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory(); self.path=Path(self.tmp.name)/'test.sqlite3'; initialize(self.path)
        self.cid=uuid4(); records.create(self.path,ConversationCreate(conversation_id=self.cid,operation_id=uuid4()))
        self.rid=self.request()
        self.settings=Settings(provider='openai',api_key='fictional-test-key',call_limit=6)
    def tearDown(self): self.tmp.cleanup()
    def request(self):
        rid=uuid4();records.submit(self.path,self.cid,MessageSubmit(request_id=rid,content='fictional history'))
        return rid
    def result(self,value=None):
        return {'status':'completed','output':[{'type':'message','role':'assistant','content':[{'type':'output_text','text':json.dumps(value or {'sql':'SELECT id FROM sessions LIMIT 1','parameters':[]})}]}],'usage':{'input_tokens':30,'output_tokens':20}}
    def call(self,handler,settings=None,stage='planning'):
        provider=Provider(self.path,self.rid,settings or self.settings,httpx.MockTransport(handler))
        return asyncio.run(provider.call(stage,'reviewed','fictional',PLAN))
    def test_configuration_is_explicit_and_secret_not_represented(self):
        path=Path(self.tmp.name)/'.env'
        self.assertEqual(load(path).provider,'mock')
        path.write_text('MODEL_PROVIDER=openai\nOPENAI_API_KEY=fictional-test-key\nLIVE_CALL_LIMIT=6\n')
        self.assertNotIn('fictional-test-key',repr(load(path)))
        self.assertEqual(load(path).model,MODEL)
        for bad in ['LIVE_CALL_LIMIT=7','MODEL_PROVIDER=other','OPENAI_API_KEY=$(unsafe)','OPENAI_API_KEY=a\nOPENAI_API_KEY=b']:
            path.write_text(bad);self.assertEqual(load(path).error,'configuration_unavailable')
    def test_missing_key_no_call_or_budget_and_history_available(self):
        called=[]
        with self.assertRaises(RAGFailure) as error:
            self.call(lambda req: called.append(req),Settings(provider='openai',call_limit=6))
        self.assertEqual(error.exception.code,'configuration_unavailable');self.assertEqual(called,[]);self.assertEqual(usage.used(self.path),0)
        with TestClient(create_app(self.path,Settings(provider='openai',call_limit=6))) as client:
            self.assertFalse(client.get('/api/health').json()['configured'])
            self.assertEqual(client.get('/api/sessions').status_code,200)
    def test_success_checked_payload_and_durable_budget(self):
        def handler(request):
            body=json.loads(request.content)
            self.assertFalse(body['store']); self.assertEqual(body['model'],MODEL)
            self.assertEqual(body['max_output_tokens'],1024);self.assertTrue(body['text']['format']['strict'])
            return httpx.Response(200,json=self.result())
        self.call(handler)
        initialize(self.path);self.assertEqual(usage.used(self.path),1)
        self.assertEqual(records.get_status(self.path,self.rid)['provider_call_count'],1)
        with self.assertRaises(RAGFailure) as error: self.call(handler)
        self.assertEqual(error.exception.code,'duplicate_call');self.assertEqual(usage.used(self.path),1)
    def test_failures_consume_budget_without_assistant(self):
        scenarios=[(lambda req:httpx.Response(503,json={'error':'fictional'}),'provider_http_503'),
                   (lambda req:httpx.Response(200,json={'status':'incomplete'}),'invalid_provider_output'),
                   (lambda req:httpx.Response(200,json=self.result({'sql':1,'parameters':[]})),'invalid_provider_output')]
        for handler,code in scenarios:
            with self.subTest(code=code):
                with self.assertRaises(RAGFailure) as error:self.call(handler)
                self.assertEqual(error.exception.code,code)
                records.fail(self.path,self.rid,code);self.rid=self.request()
        self.assertEqual(usage.used(self.path),3)
        self.assertTrue(all(m['role']=='user' for m in records.list_messages(self.path,self.cid,0,100)['messages']))
    def test_timeout_refusal_and_limit_no_network_after_six(self):
        def timeout(req):raise httpx.ReadTimeout('fictional')
        for handler,code in [(timeout,'provider_timeout'),(lambda req:httpx.Response(200,json={'status':'completed','output':[{'type':'message','role':'assistant','content':[{'type':'refusal','refusal':'no'}]}]}),'provider_refusal')]:
            with self.assertRaises(RAGFailure) as error:self.call(handler)
            self.assertEqual(error.exception.code,code);records.fail(self.path,self.rid,code);self.rid=self.request()
        for _ in range(4):
            self.call(lambda req:httpx.Response(200,json=self.result()))
            records.fail(self.path,self.rid,'test');self.rid=self.request()
        called=[]
        with self.assertRaises(RAGFailure) as error:self.call(lambda req:called.append(req))
        self.assertEqual(error.exception.code,'budget_exhausted');self.assertEqual(called,[])
        initialize(self.path);self.assertEqual(usage.used(self.path),6)

    def test_two_http_stages_save_actual_reply_and_failure_keeps_user(self):
        from unittest.mock import patch
        from backend.app.controllers.conversations import generate
        def handler(req):
            body=json.loads(req.content)
            if body['text']['format']['name']=='planning':
                return httpx.Response(200,json=self.result())
            return httpx.Response(200,json=self.result({'content':'No matching fictional sessions are saved.','citations':[]}))
        provider=Provider(self.path,self.rid,self.settings,httpx.MockTransport(handler))
        with patch('backend.app.providers.openai.Provider',return_value=provider):
            asyncio.run(generate(self.path,self.rid,settings=self.settings))
        status=records.get_status(self.path,self.rid)
        self.assertEqual(status['status'],'succeeded');self.assertEqual(status['provider_call_count'],2)
        self.assertEqual(status['assistant_content'],'No matching fictional sessions are saved.')
        self.assertEqual(usage.used(self.path),2)
        self.rid=self.request()
        provider=Provider(self.path,self.rid,self.settings,httpx.MockTransport(lambda req:httpx.Response(503)))
        with patch('backend.app.providers.openai.Provider',return_value=provider):
            asyncio.run(generate(self.path,self.rid,settings=self.settings))
        status=records.get_status(self.path,self.rid)
        self.assertEqual(status['error_code'],'provider_http_503');self.assertIsNone(status['assistant_message_id'])
        self.assertEqual(status['provider_call_count'],1);self.assertEqual(usage.used(self.path),3)
