import os
from pathlib import Path
import tempfile
import unittest
from uuid import uuid4
from fastapi.testclient import TestClient
from backend.app.main import create_app
from backend.app.db import DATABASE_PATH, PROJECT_ROOT, connect


class SessionsTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.path = Path(self.tmp.name) / 'test.sqlite3'
        self.client = TestClient(create_app(self.path))
        self.client.__enter__()
        self.body = dict(session_id=str(uuid4()), operation_id=str(uuid4()),
                         skill_key='paced_breathing_4_6', started_at='2026-10-21T12:00:00Z')

    def tearDown(self):
        self.client.__exit__(None, None, None)
        self.tmp.cleanup()

    def counts(self):
        db = connect(self.path)
        try:
            return tuple(db.execute('SELECT COUNT(*) FROM ' + table).fetchone()[0]
                         for table in ('exercise_sessions', 'operations'))
        finally:
            db.close()

    def test_save_read_replay_and_restart(self):
        first = self.client.post('/api/sessions', json=self.body)
        self.assertEqual(first.status_code, 201)
        expected = first.json()['session']
        self.assertEqual(expected['status'], 'in_progress')
        self.assertEqual(expected['active_duration_ms'], 0)
        replay = self.client.post('/api/sessions', json=self.body)
        self.assertEqual(replay.status_code, 200)
        self.assertTrue(replay.json()['replayed'])
        self.assertEqual(replay.json()['session'], expected)
        with TestClient(create_app(self.path)) as restarted:
            got = restarted.get('/api/sessions/' + self.body['session_id'])
            self.assertEqual(got.json()['session'], expected)
        self.assertEqual(self.counts(), (1, 1))

    def test_conflicting_operation_and_session_ids(self):
        self.client.post('/api/sessions', json=self.body)
        for change in ({'started_at': '2026-10-21T13:00:00Z'}, {'operation_id': str(uuid4())}):
            response = self.client.post('/api/sessions', json=self.body | change)
            self.assertEqual(response.status_code, 409)
        self.assertEqual(self.counts(), (1, 1))

    def test_invalid_inputs_do_not_write(self):
        for change in ({'session_id': 'invalid'}, {'skill_key': "'; DROP TABLE exercise_sessions; --"},
                       {'started_at': '2026-10-21T12:00:00'}, {'demo_user_id': str(uuid4())}):
            self.assertEqual(self.client.post('/api/sessions', json=self.body | change).status_code, 422)
        self.assertEqual(self.counts(), (0, 0))

    def test_missing_record(self):
        self.assertEqual(self.client.get('/api/sessions/' + str(uuid4())).status_code, 404)

    def test_failed_operation_insert_rolls_back_session(self):
        db = connect(self.path)
        try:
            db.execute("CREATE TRIGGER fail_operation BEFORE INSERT ON operations BEGIN SELECT RAISE(ABORT, 'test failure'); END")
            db.commit()
        finally:
            db.close()
        response = self.client.post('/api/sessions', json=self.body)
        self.assertEqual(response.status_code, 503)
        self.assertNotEqual(response.json()['persistence'], 'saved')
        self.assertEqual(self.counts(), (0, 0))

    def test_path_independent_of_working_directory(self):
        previous = Path.cwd()
        try:
            os.chdir(self.tmp.name)
            self.assertEqual(DATABASE_PATH, PROJECT_ROOT / 'data' / 'app.sqlite3')
            self.assertTrue(DATABASE_PATH.is_absolute())
        finally:
            os.chdir(previous)


if __name__ == '__main__':
    unittest.main()


class SessionIntegrationTest(unittest.TestCase):
    tearDown = SessionsTest.tearDown
    counts = SessionsTest.counts
    def setUp(self):
        SessionsTest.setUp(self)
        self.body['owner_token'] = str(uuid4())
        self.client.post('/api/sessions', json=self.body)
        self.url = '/api/sessions/' + self.body['session_id']

    # Only the additional integration cases; inherited cases use a fresh unseeded fixture.
    def test_finalize_replay_and_history(self):
        body = dict(operation_id=str(uuid4()), owner_token=self.body['owner_token'], expected_revision=1,
                    status='completed', active_duration_ms=60000, paused_duration_ms=0, ended_at='2026-10-21T12:01:00Z')
        response = self.client.put(self.url, json=body)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['session']['revision'], 2)
        self.assertTrue(self.client.put(self.url, json=body).json()['replayed'])
        self.assertEqual(self.counts(), (1, 2))
        changed = body | {'operation_id': str(uuid4()), 'expected_revision': 2, 'status': 'stopped'}
        self.assertEqual(self.client.put(self.url, json=changed).status_code, 409)
        rows = self.client.get('/api/sessions').json()['sessions']
        self.assertEqual(rows[0]['status'], 'completed')
        self.assertNotIn('owner_token', rows[0])

    def test_owner_revision_and_recovery(self):
        base = dict(operation_id=str(uuid4()), owner_token=self.body['owner_token'], expected_revision=1,
                    status='in_progress', active_duration_ms=5000, paused_duration_ms=0, ended_at=None)
        self.assertEqual(self.client.put(self.url, json=base | {'owner_token': str(uuid4())}).status_code, 409)
        self.assertEqual(self.client.put(self.url, json=base).status_code, 200)
        interrupted = base | {'operation_id': str(uuid4()), 'status': 'interrupted', 'expected_revision': 2, 'ended_at': '2026-10-21T12:01:00Z'}
        self.assertEqual(self.client.put(self.url, json=interrupted | {'active_duration_ms': 6000}).status_code, 409)
        self.assertEqual(self.client.put(self.url, json=interrupted).status_code, 200)
        self.assertEqual(self.client.get(self.url).json()['session']['active_duration_ms'], 5000)

    def test_terminal_validation(self):
        body = dict(operation_id=str(uuid4()), owner_token=self.body['owner_token'], expected_revision=1,
                    status='completed', active_duration_ms=12000, paused_duration_ms=0, ended_at='2026-10-21T12:01:00Z')
        self.assertEqual(self.client.put(self.url, json=body).status_code, 422)
