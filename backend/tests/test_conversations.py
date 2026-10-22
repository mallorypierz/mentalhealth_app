import sqlite3
import tempfile
import time
import unittest
from pathlib import Path
from uuid import uuid4
from fastapi.testclient import TestClient
from backend.app.main import create_app
from backend.app.db import connect

class ConversationTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory(); self.path=Path(self.tmp.name)/'test.sqlite3'
        self.client=TestClient(create_app(self.path)); self.client.__enter__()
        self.conv={'conversation_id':str(uuid4()),'operation_id':str(uuid4())}
        self.assertEqual(self.client.post('/api/conversations',json=self.conv).status_code,201)
        self.url='/api/conversations/'+self.conv['conversation_id']+'/messages'
        self.body={'request_id':str(uuid4()),'content':'Fictional question: how do I stop practice?','mock_mode':'success'}

    def tearDown(self):
        self.client.__exit__(None,None,None); self.tmp.cleanup()

    def finish(self,ident=None):
        ident=ident or self.body['request_id']
        for _ in range(100):
            value=self.client.get('/api/requests/'+ident).json()
            if value['status']!='pending': return value
            time.sleep(.02)
        self.fail('Mock request did not finish')

    def rows(self):
        return self.client.get(self.url).json()['messages']

    def trigger(self,sql):
        db=connect(self.path)
        try: db.executescript(sql)
        finally: db.close()

    def test_success_duplicate_and_restart(self):
        self.assertEqual(self.client.post('/api/conversations',json=self.conv).status_code,200)
        for _ in range(2): self.assertEqual(self.client.post(self.url,json=self.body).status_code,202)
        result=self.finish(); self.assertEqual(result['status'],'succeeded'); self.assertEqual(result['provider_call_count'],2)
        rows=self.rows(); self.assertEqual([r['role'] for r in rows],['user','assistant'])
        self.assertEqual([r['sequence'] for r in rows],[1,2])
        self.assertEqual(rows[1]['content'],result['assistant_content'])
        with TestClient(create_app(self.path)) as restarted:
            self.assertEqual(restarted.get(self.url).json()['messages'],rows)

    def test_failure_retry_without_duplicate_user(self):
        self.body['mock_mode']='failure'; self.client.post(self.url,json=self.body)
        result=self.finish(); self.assertEqual(result['error_code'],'provider_failure')
        self.assertIsNone(result['assistant_message_id']); self.assertEqual(len(self.rows()),1)
        retry={'operation_id':str(uuid4()),'mock_mode':'success'}
        url='/api/requests/'+self.body['request_id']+'/retry'
        self.assertEqual(self.client.post(url,json=retry).status_code,202)
        self.assertEqual(self.client.post(url,json=retry).status_code,202)
        result=self.finish(); self.assertEqual(result['attempt_count'],2); self.assertEqual(result['provider_call_count'],3)
        self.assertEqual([r['role'] for r in self.rows()],['user','assistant'])

    def test_initial_save_failure_rolls_back_without_reply(self):
        self.trigger("CREATE TRIGGER fail_user BEFORE INSERT ON messages WHEN NEW.role='user' BEGIN SELECT RAISE(ABORT,'test'); END;")
        self.assertEqual(self.client.post(self.url,json=self.body).status_code,503)
        self.assertEqual(self.client.get('/api/requests/'+self.body['request_id']).status_code,404)
        self.assertEqual(self.rows(),[])

    def test_reply_save_failure_has_no_assistant_then_retry(self):
        self.trigger("CREATE TRIGGER fail_reply BEFORE INSERT ON messages WHEN NEW.role='assistant' BEGIN SELECT RAISE(ABORT,'test'); END;")
        self.client.post(self.url,json=self.body); result=self.finish()
        self.assertEqual(result['error_code'],'reply_save_failed'); self.assertEqual(result['assistant_persistence'],'not_saved')
        self.assertEqual(len(self.rows()),1)
        self.trigger('DROP TRIGGER fail_reply;')
        self.client.post('/api/requests/'+self.body['request_id']+'/retry',json={'operation_id':str(uuid4()),'mock_mode':'success'})
        self.assertEqual(self.finish()['status'],'succeeded'); self.assertEqual(len(self.rows()),2)

    def test_validation_and_conflicting_submissions(self):
        self.assertEqual(self.client.post(self.url,json=self.body|{'content':'   '}).status_code,422)
        self.body['mock_mode']='delayed'; self.client.post(self.url,json=self.body)
        self.assertEqual(self.client.post(self.url,json=self.body|{'content':'different'}).status_code,409)
        self.assertEqual(self.client.post(self.url,json=self.body|{'request_id':str(uuid4())}).status_code,409)
        self.assertEqual(len(self.rows()),1)

    def test_interrupted_request_not_regenerated_on_restart(self):
        self.body['mock_mode']='delayed'; self.client.post(self.url,json=self.body)
        self.client.__exit__(None,None,None)
        self.client=TestClient(create_app(self.path)); self.client.__enter__()
        result=self.client.get('/api/requests/'+self.body['request_id']).json()
        self.assertEqual(result['status'],'failed'); self.assertEqual(result['error_code'],'interrupted')
        self.assertEqual(len(self.rows()),1)

    def test_ownership_scope_and_pagination(self):
        self.client.post(self.url,json=self.body); self.finish()
        first=self.client.get(self.url+'?limit=1').json(); second=self.client.get(self.url+'?cursor='+str(first['next_cursor'])).json()
        self.assertEqual(first['messages'][0]['sequence'],1); self.assertEqual(second['messages'][0]['sequence'],2)
        self.trigger("INSERT INTO demo_users VALUES ('other','Other fictional user'); UPDATE conversations SET demo_user_id='other';")
        self.assertEqual(self.client.get(self.url).status_code,404)
        self.assertEqual(self.client.get('/api/requests/'+self.body['request_id']).status_code,404)
        self.assertEqual(self.client.get('/api/conversations').json()['conversations'],[])
