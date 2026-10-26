"""Isolated fictional fixtures; these do not insert events in the working database."""
from datetime import datetime, timedelta
from pathlib import Path
import tempfile
import unittest
from uuid import uuid4
from fastapi.testclient import TestClient
from backend.app.main import create_app
from backend.app.db import connect


def uid(): return str(uuid4())


class CalendarTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.path = Path(self.tmp.name) / 'test.sqlite3'
        self.client = TestClient(create_app(self.path, enable_profiles=True))
        self.client.__enter__()
        self.a, self.owner = self.profile('Fictional A')
        self.b, _ = self.profile('Fictional B')

    def tearDown(self):
        self.client.__exit__(None, None, None)
        self.tmp.cleanup()

    def profile(self, name):
        token = self.client.post('/api/identity/bootstrap', json={'bootstrap_id': uid()}).json()['access_token']
        headers = {'Authorization': 'Bearer ' + token}
        owner = uid()
        self.assertEqual(self.client.post('/api/profiles', headers=headers, json=dict(profile_id=owner, operation_id=uid(), display_name=name)).status_code, 201)
        result = self.client.post('/api/identity/select', headers=headers, json=dict(profile_id=owner, operation_id=uid(), expected_context_version=1))
        self.assertEqual(result.status_code, 200)
        headers['X-Context-Version'] = str(result.json()['context_version'])
        return headers, owner

    def session(self, ended, status='completed', headers=None):
        h = headers or self.a
        end = datetime.fromisoformat(ended)
        sid, token = uid(), uid()
        create = dict(session_id=sid, operation_id=uid(), owner_token=token, skill_key='paced_breathing_4_6', started_at=(end-timedelta(seconds=60)).isoformat())
        r = self.client.post('/api/sessions', headers=h, json=create)
        self.assertEqual(r.status_code, 201, r.text)
        body = dict(operation_id=uid(), owner_token=token, expected_revision=1, status=status, active_duration_ms=60000 if status=='completed' else (0 if status=='interrupted' else 10000), paused_duration_ms=0, ended_at=ended)
        r = self.client.put('/api/sessions/'+sid, headers=h, json=body)
        self.assertEqual(r.status_code, 200, r.text)
        duplicate = self.client.put('/api/sessions/'+sid, headers=h, json=body)
        self.assertTrue(duplicate.json()['replayed'])
        return sid

    def calendar(self, month='2026-11', zone='America/New_York', headers=None):
        r = self.client.get('/api/calendar', headers=headers or self.a, params={'month':month, 'timezone':zone})
        self.assertEqual(r.status_code, 200, r.text)
        return r.json()['events']

    def test_empty_multiple_completion_midnight_month_and_isolation(self):
        self.assertEqual(self.calendar(), [])
        october = self.session('2026-11-01T03:59:59+00:00')
        first = self.session('2026-11-01T04:00:00+00:00')
        second = self.session('2026-11-01T04:01:00+00:00')
        self.session('2026-11-01T04:02:00+00:00','stopped')
        self.session('2026-11-01T04:03:00+00:00','interrupted')
        self.session('2026-11-01T04:04:00+00:00',headers=self.b)
        events = self.calendar()
        self.assertEqual([e['session_id'] for e in events], [first,second])
        self.assertEqual({e['local_date'] for e in events},{'2026-11-01'})
        self.assertEqual([e['session_id'] for e in self.calendar('2026-10')],[october])
        self.assertEqual(len(self.calendar(zone='UTC')),3)
        self.assertEqual(len(self.calendar(headers=self.b)),1)
        self.assertEqual(self.client.get('/api/sessions/'+first,headers=self.b).status_code,404)
        with connect(self.path) as db:
            row = db.execute('SELECT * FROM exercise_sessions WHERE id=?',(first,)).fetchone()
            self.assertEqual(row['demo_user_id'],self.owner)
            self.assertEqual(datetime.fromisoformat(row['ended_at']),datetime.fromisoformat(events[0]['completed_at']))
            self.assertEqual(row['active_duration_ms'],events[0]['active_duration_ms'])
        self.assertEqual(self.calendar(),events)  # repeated refresh
        with TestClient(create_app(self.path,enable_profiles=True)) as restarted:
            self.assertEqual(restarted.get('/api/calendar',headers=self.a,params={'month':'2026-11','timezone':'America/New_York'}).json()['events'], events)

    def test_dst_offsets_pagination_validation_and_stale_access(self):
        self.session('2026-11-01T05:30:00+00:00')
        self.session('2026-11-01T06:30:00+00:00')
        events=self.calendar()
        self.assertTrue(events[0]['local_time'].endswith('-04:00'))
        self.assertTrue(events[1]['local_time'].endswith('-05:00'))
        page=self.client.get('/api/calendar?month=2026-11&timezone=UTC&limit=1',headers=self.a).json()
        self.assertEqual(page['next_cursor'],1)
        for zone,month in [('invalid/zone','2026-11'),('UTC','2026-13')]:
            self.assertEqual(self.client.get('/api/calendar',headers=self.a,params={'month':month,'timezone':zone}).status_code,422)
        self.assertEqual(self.client.get('/api/calendar?month=2026-11&timezone=UTC').status_code,401)
        h=self.a|{'X-Context-Version':'1'}
        self.assertEqual(self.client.get('/api/calendar?month=2026-11&timezone=UTC',headers=h).status_code,409)

    def test_guest_transfer_delete_and_rag_ownership(self):
        import time
        token=self.client.post('/api/identity/bootstrap',json={'bootstrap_id':uid()}).json()['access_token']
        guest={'Authorization':'Bearer '+token}
        response=self.client.post('/api/identity/guest',headers=guest,json={'operation_id':uid(),'expected_context_version':1})
        self.assertEqual(response.status_code,200,response.text)
        guest['X-Context-Version']='2'
        sid=self.session('2026-11-02T12:00:00+00:00',headers=guest)
        self.session('2026-11-03T12:00:00+00:00',headers=self.a)
        cid=uid()
        self.assertEqual(self.client.post('/api/conversations',headers=guest,json={'conversation_id':cid,'operation_id':uid()}).status_code,201)
        rid=uid()
        self.client.post('/api/conversations/'+cid+'/messages',headers=guest,json={'request_id':rid,'content':'What happened in my last breathing practice?','mock_mode':'success'})
        for _ in range(100):
            r=self.client.get('/api/requests/'+rid,headers=guest).json()
            if r['status']!='pending': break
            time.sleep(.02)
        self.assertEqual(r['status'],'succeeded',r)
        self.assertIn(sid,r['assistant_content'])
        self.assertEqual(self.client.get('/api/conversations/'+cid+'/messages',headers=self.a).status_code,404)
        self.assertEqual(self.client.get('/api/requests/'+rid,headers=self.b).status_code,404)
        transfer={'operation_id':uid(),'expected_context_version':2,'profile_id':self.owner,'guest_disposition':'save'}
        r=self.client.post('/api/identity/select',headers=guest,json=transfer)
        self.assertEqual(r.status_code,200,r.text)
        self.assertTrue(self.client.post('/api/identity/select',headers=guest,json=transfer).json()['replayed'])
        self.assertEqual(len(self.calendar()),2)
        self.assertEqual(self.client.get('/api/conversations/'+cid+'/messages',headers=self.a).status_code,200)
        self.assertEqual(self.client.get('/api/calendar?month=2026-11&timezone=UTC',headers=guest).status_code,409)
        guest['X-Context-Version']='3'
        deletion={'operation_id':uid(),'expected_context_version':3,'expected_revision':1,'confirm_delete':True}
        r=self.client.post('/api/profile/delete',headers=guest,json=deletion)
        self.assertEqual(r.status_code,200,r.text)
        self.assertTrue(self.client.post('/api/profile/delete',headers=guest,json=deletion).json()['replayed'])
        self.assertEqual(self.client.get('/api/calendar?month=2026-11&timezone=UTC',headers=self.a).status_code,401)
        with connect(self.path) as db:
            self.assertEqual(db.execute('SELECT COUNT(*) FROM exercise_sessions WHERE demo_user_id=?',(self.owner,)).fetchone()[0],0)

    def test_guest_refresh_restart_discard_and_active_switch_guard(self):
        token=self.client.post('/api/identity/bootstrap',json={'bootstrap_id':uid()}).json()['access_token']
        h={'Authorization':'Bearer '+token}
        guest=self.client.post('/api/identity/guest',headers=h,json={'operation_id':uid(),'expected_context_version':1}).json()
        h['X-Context-Version']='2'
        self.assertEqual(self.client.get('/api/identity',headers=h).json()['active_owner_id'],guest['active_owner_id'])
        sid,ownership=uid(),uid()
        self.client.post('/api/sessions',headers=h,json={'session_id':sid,'operation_id':uid(),'owner_token':ownership,'skill_key':'paced_breathing_4_6','started_at':'2026-10-25T12:00:00Z'})
        switch={'operation_id':uid(),'expected_context_version':2,'profile_id':self.owner,'guest_disposition':'discard'}
        self.assertEqual(self.client.post('/api/identity/select',headers=h,json=switch).status_code,409)
        self.client.put('/api/sessions/'+sid,headers=h,json={'operation_id':uid(),'owner_token':ownership,'expected_revision':1,'status':'stopped','active_duration_ms':1000,'paused_duration_ms':0,'ended_at':'2026-10-25T12:00:01Z'})
        with TestClient(create_app(self.path,enable_profiles=True)) as restarted:
            self.assertEqual(restarted.get('/api/sessions/'+sid,headers=h).status_code,200)
        leave={'operation_id':uid(),'expected_context_version':2,'confirm_discard':True}
        self.assertEqual(self.client.post('/api/identity/leave',headers=h,json=leave).status_code,200)
        self.assertTrue(self.client.post('/api/identity/leave',headers=h,json=leave).json()['replayed'])
        with connect(self.path) as db:
            self.assertIsNone(db.execute('SELECT id FROM exercise_sessions WHERE id=?',(sid,)).fetchone())
        self.assertEqual(self.calendar(),[])
