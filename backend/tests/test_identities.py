from pathlib import Path
from datetime import datetime
import sqlite3
import tempfile
import unittest
from uuid import uuid4

from fastapi.testclient import TestClient

from backend.app.db import DEMO_USER_ID, connect, initialize, migrate_identities
from backend.app.main import create_app


def uid():
    return str(uuid4())


class IdentityFoundationTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.path = Path(self.tmp.name) / 'profiles.sqlite3'
        self.client = TestClient(create_app(self.path, enable_profiles=True))
        self.client.__enter__()
        self.headers = self.bootstrap()

    def tearDown(self):
        self.client.__exit__(None, None, None)
        self.tmp.cleanup()

    def bootstrap(self):
        response = self.client.post('/api/identity/bootstrap', json={'bootstrap_id': uid()})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.headers['cache-control'], 'no-store')
        return {'Authorization': 'Bearer ' + response.json()['access_token']}

    def create(self, name='Fictional Alex', headers=None, **fields):
        body = dict(profile_id=uid(), operation_id=uid(), display_name=name, **fields)
        response = self.client.post('/api/profiles', json=body, headers=headers or self.headers)
        self.assertEqual(response.status_code, 201)
        return body, response.json()['profile']

    def select(self, profile, headers=None):
        body = dict(profile_id=profile['id'], operation_id=uid(), expected_context_version=1)
        response = self.client.post('/api/identity/select', json=body, headers=headers or self.headers)
        self.assertEqual(response.status_code, 200)
        return body, response.json()

    def test_save_read_duplicate_refresh_and_app_restart(self):
        body, profile = self.create('  Fictional Alex  ', age=21, gender=None)
        self.assertEqual(profile['display_name'], 'Fictional Alex')
        self.assertEqual(profile['revision'], 1)
        duplicate = self.client.post('/api/profiles', json=body, headers=self.headers)
        self.assertEqual(duplicate.status_code, 200)
        self.assertTrue(duplicate.json()['replayed'])
        selection, identity = self.select(profile)
        self.assertEqual(identity['context_version'], 2)
        self.assertEqual(identity['authentication'], 'local_chooser_not_authentication')
        self.assertTrue(self.client.post('/api/identity/select', json=selection,
                                       headers=self.headers).json()['replayed'])
        # Repeated reads model an API refresh; this is not a browser/UI test.
        for _ in range(2):
            self.assertEqual(self.client.get('/api/profile', headers=self.headers).json()['profile'], profile)
        with TestClient(create_app(self.path, enable_profiles=True)) as restarted:
            self.assertEqual(restarted.get('/api/profile', headers=self.headers).json()['profile'], profile)
        with connect(self.path) as db:
            self.assertEqual(db.execute("SELECT count(*) FROM demo_users WHERE kind='profile'").fetchone()[0], 1)
            row = dict(db.execute('SELECT * FROM demo_users WHERE id=?', (profile['id'],)).fetchone())
            for key, value in profile.items():
                if key in ('created_at', 'updated_at'):
                    self.assertEqual(datetime.fromisoformat(row[key]), datetime.fromisoformat(value))
                else:
                    self.assertEqual(row[key], value)

    def test_optional_fields_blank_and_duplicate_display_names(self):
        _, first = self.create(gender='   ')
        _, second = self.create()
        self.assertIsNone(first['age'])
        self.assertIsNone(first['gender'])
        self.assertNotEqual(first['id'], second['id'])
        listing = self.client.get('/api/profiles', headers=self.headers).json()['profiles']
        self.assertEqual(len(listing), 2)
        self.assertEqual(set(listing[0]), {'id', 'display_name', 'created_at'})

    def test_profile_detail_reads_bound_to_token_not_client_profile_id(self):
        other_headers = self.bootstrap()
        _, alex = self.create(age=21)
        _, sam = self.create('Fictional Sam', headers=other_headers, age=30)
        self.select(alex)
        self.select(sam, other_headers)
        self.assertEqual(self.client.get('/api/profile?profile_id=' + sam['id'],
                                        headers=self.headers).json()['profile']['id'], alex['id'])
        self.assertEqual(self.client.get('/api/profile', headers=other_headers).json()['profile']['id'], sam['id'])
        for headers in ({}, {'Authorization': 'Bearer ' + sam['id']}, {'Authorization': 'Bearer ' + 'x' * 43}):
            self.assertEqual(self.client.get('/api/profile', headers=headers).status_code, 401)
        self.assertEqual(self.client.get('/api/profile', headers=self.bootstrap()).status_code, 409)

    def test_revoked_token_and_no_plaintext_token_storage(self):
        token = self.headers['Authorization'][7:]
        with connect(self.path) as db:
            rows = [dict(row) for row in db.execute('SELECT * FROM browser_sessions')]
            self.assertNotIn(token, str(rows))
            db.execute("UPDATE browser_sessions SET revoked_at='2026-10-25T12:00:00Z'")
        self.assertEqual(self.client.get('/api/profiles', headers=self.headers).status_code, 401)

    def test_conflicting_ids_and_stale_context(self):
        body, profile = self.create()
        for change in ({'display_name': 'Changed'}, {'operation_id': uid()}):
            self.assertEqual(self.client.post('/api/profiles', json=body | change,
                                             headers=self.headers).status_code, 409)
        self.assertEqual(self.client.post('/api/profiles', json=body, headers=self.bootstrap()).status_code, 409)
        stale = dict(profile_id=profile['id'], operation_id=uid(), expected_context_version=99)
        self.assertEqual(self.client.post('/api/identity/select', json=stale, headers=self.headers).status_code, 409)

    def test_validation_and_parameterized_name(self):
        base = dict(profile_id=uid(), operation_id=uid(), display_name='Fictional')
        for change in ({'display_name': '  '}, {'display_name': 'x' * 61}, {'age': True}, {'age': 2.5},
                       {'age': -1}, {'age': 121}, {'age': '20'}, {'gender': 'x' * 61},
                       {'password': 'not-supported'}, {'demo_user_id': uid()}):
            self.assertEqual(self.client.post('/api/profiles', json=base | change,
                                             headers=self.headers).status_code, 422)
        name = "Fictional'); DROP TABLE demo_users; --"
        _, profile = self.create(name)
        self.assertEqual(profile['display_name'], name)
        self.assertEqual(len(self.client.get('/api/profiles', headers=self.headers).json()['profiles']), 1)

    def test_failed_operation_rolls_back_profile_and_retry_saves_once(self):
        body = dict(profile_id=uid(), operation_id=uid(), display_name='Fictional rollback')
        with connect(self.path) as db:
            db.execute("CREATE TRIGGER fail_identity BEFORE INSERT ON identity_operations "
                       "BEGIN SELECT RAISE(ABORT, 'test failure'); END")
        response = self.client.post('/api/profiles', json=body, headers=self.headers)
        self.assertEqual(response.status_code, 503)
        self.assertEqual(response.json()['persistence'], 'unknown')
        with connect(self.path) as db:
            self.assertEqual(db.execute("SELECT count(*) FROM demo_users WHERE kind='profile'").fetchone()[0], 0)
            db.execute('DROP TRIGGER fail_identity')
        self.assertEqual(self.client.post('/api/profiles', json=body, headers=self.headers).status_code, 201)
        self.assertTrue(self.client.post('/api/profiles', json=body, headers=self.headers).json()['replayed'])

    def test_legacy_not_selectable_and_bootstrap_not_a_token_recovery_endpoint(self):
        self.assertEqual(self.client.get('/api/profiles', headers=self.headers).json()['profiles'], [])
        body = dict(profile_id=DEMO_USER_ID, operation_id=uid(), expected_context_version=1)
        self.assertEqual(self.client.post('/api/identity/select', json=body, headers=self.headers).status_code, 404)
        self.assertEqual(self.client.post('/api/profiles', headers=self.headers,
            json=dict(profile_id=DEMO_USER_ID, operation_id=uid(), display_name='New person')).status_code, 409)
        current = self.client.get('/api/identity', headers=self.headers).json()
        response = self.client.post('/api/identity/bootstrap', json={'bootstrap_id': current['browser_session_id']})
        self.assertEqual(response.status_code, 409)
        self.assertNotIn('access_token', response.json())
        denied = self.client.post('/api/identity/bootstrap', json={'bootstrap_id': uid()},
                                  headers={'Origin': 'https://unrelated.example'})
        self.assertEqual(denied.status_code, 403)


class IdentityMigrationTest(unittest.TestCase):
    def test_existing_data_preserved_and_migration_runs_once(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / 'legacy.sqlite3'
            with TestClient(create_app(path)) as client:
                client.post('/api/sessions', json=dict(session_id=uid(), operation_id=uid(),
                    skill_key='paced_breathing_4_6', started_at='2026-10-22T12:00:00Z'))
                client.post('/api/conversations', json=dict(conversation_id=uid(), operation_id=uid()))
            tables = ['exercise_sessions', 'conversations', 'operations', 'conversation_operations',
                      'messages', 'requests', 'provider_attempts']
            def snapshot():
                with connect(path) as db:
                    return {table: [tuple(r) for r in db.execute('SELECT * FROM ' + table)] for table in tables}
            before = snapshot()
            initialize(path, enable_profiles=True)
            initialize(path, enable_profiles=True)
            self.assertEqual(snapshot(), before)
            with connect(path) as db:
                row = db.execute('SELECT * FROM demo_users').fetchone()
                self.assertEqual(row['id'], DEMO_USER_ID)
                self.assertEqual(row['display_name'], 'Fictional coursework student')
                self.assertEqual(row['kind'], 'legacy')
                self.assertIsNone(row['created_at'])  # Do not invent a historical creation date.
                self.assertEqual(db.execute('SELECT count(*) FROM schema_migrations WHERE version=4').fetchone()[0], 1)
                self.assertEqual(db.execute('PRAGMA foreign_key_check').fetchall(), [])

    def test_failed_migration_rolls_back_all_added_columns(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / 'legacy.sqlite3'
            initialize(path)
            with connect(path) as db:
                db.execute('CREATE TABLE browser_sessions(existing TEXT)')
            db = connect(path)
            try:
                with self.assertRaises(sqlite3.OperationalError):
                    migrate_identities(db)
                self.assertEqual([r[1] for r in db.execute('PRAGMA table_info(demo_users)')], ['id', 'display_name'])
            finally:
                db.close()


if __name__ == '__main__':
    unittest.main()
