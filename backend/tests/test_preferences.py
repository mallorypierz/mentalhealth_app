import unittest
from backend.tests import test_calendar
uid = test_calendar.uid
from fastapi.testclient import TestClient
from backend.app.main import create_app
from backend.app.db import connect

class PreferencesTest(unittest.TestCase):
    setUp = test_calendar.CalendarTest.setUp
    tearDown = test_calendar.CalendarTest.tearDown
    profile = test_calendar.CalendarTest.profile
    def test_preferences_isolation_retry_forget_restart(self):
        body = dict(operation_id=uid(), expected_revision=0, answers=dict(activity='stop', breath='yes'))
        response = self.client.put('/api/preferences', headers=self.a, json=body)
        self.assertEqual(response.status_code,200)
        self.assertEqual(response.json()['id'],self.owner)
        self.assertIsNone(self.client.get('/api/preferences',headers=self.b).json()['answers'])
        self.assertTrue(self.client.put('/api/preferences',headers=self.a,json=body).json()['replayed'])
        with TestClient(create_app(self.path,enable_profiles=True)) as restarted:
            self.assertEqual(restarted.get('/api/preferences',headers=self.a).json()['answers'],body['answers'])
        forget=dict(operation_id=uid(),expected_revision=1,answers=None)
        self.assertEqual(self.client.put('/api/preferences',headers=self.a,json=forget).status_code,200)
        self.assertIsNone(self.client.put('/api/preferences',headers=self.a,json=body).json()['answers'])
        with connect(self.path) as db:
            self.assertEqual(db.execute('SELECT count(*) FROM preferences').fetchone()[0],1)
            self.assertIsNone(db.execute('SELECT answers FROM preferences').fetchone()[0])

    def test_failed_save_rolls_back_and_retry_is_single_write(self):
        with connect(self.path) as db:
            db.execute("CREATE TRIGGER fail_preference BEFORE INSERT ON preference_operations BEGIN SELECT RAISE(ABORT,'fictional failure'); END")
        body=dict(operation_id=uid(),expected_revision=0,answers=dict(activity='cognitive_reframe',breath='avoid'))
        self.assertEqual(self.client.put('/api/preferences',headers=self.a,json=body).status_code,503)
        self.assertIsNone(self.client.get('/api/preferences',headers=self.a).json()['answers'])
        with connect(self.path) as db: db.execute('DROP TRIGGER fail_preference')
        self.assertEqual(self.client.put('/api/preferences',headers=self.a,json=body).json()['revision'],1)
        self.assertEqual(self.client.put('/api/preferences',headers=self.a,json=body).json()['revision'],1)
        stale=dict(self.a, **{'X-Context-Version':'999'})
        self.assertEqual(self.client.put('/api/preferences',headers=stale,json=body).status_code,409)
        self.assertEqual(self.client.put('/api/preferences',headers=self.a,json=body|{'operation_id':uid()}).status_code,409)
