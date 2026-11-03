import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from uuid import uuid4

from fastapi.testclient import TestClient
from backend.app.main import create_app
from backend.app.db import connect, initialize
from backend.app.exercises import EXERCISES
from backend.app.repositories import sessions
from backend.app.schemas import SessionCreate
from backend.app.calendar import events


class ExerciseContracts(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.path = Path(self.tmp.name) / 'fictional.sqlite3'

    def tearDown(self):
        self.tmp.cleanup()

    def create_body(self, skill):
        return dict(session_id=str(uuid4()), operation_id=str(uuid4()), owner_token=str(uuid4()),
                    skill_key=skill, started_at='2026-11-02T12:00:00Z')

    def test_each_exercise_validates_its_duration_replays_and_survives_restart(self):
        with TestClient(create_app(self.path)) as client:
            for skill, (name, duration) in EXERCISES.items():
                create = self.create_body(skill)
                self.assertEqual(client.post('/api/sessions', json=create).status_code, 201)
                url = '/api/sessions/' + create['session_id']
                final = dict(operation_id=str(uuid4()), owner_token=create['owner_token'], expected_revision=1,
                             status='completed', active_duration_ms=duration, paused_duration_ms=0,
                             ended_at='2026-11-02T12:01:15Z')
                wrong = 75001 if duration == 75000 else 75000
                self.assertEqual(client.put(url, json=final | {'active_duration_ms': wrong}).status_code, 422)
                self.assertEqual(client.get(url).json()['session']['revision'], 1)
                saved = client.put(url, json=final)
                self.assertEqual(saved.status_code, 200)
                self.assertEqual(saved.json()['session']['skill_key'], skill)
                self.assertTrue(client.put(url, json=final).json()['replayed'])
            calendar = events(self.path, '2026-11', 'UTC', 0, 100)['events']
            self.assertEqual({e['exercise_name'] for e in calendar}, {e[0] for e in EXERCISES.values()})
        with TestClient(create_app(self.path)) as client:
            rows = client.get('/api/sessions').json()['sessions']
            self.assertEqual(len(rows), 4)
            self.assertTrue(all(row['status'] == 'completed' for row in rows))
        with connect(self.path) as db:
            self.assertEqual(db.execute('PRAGMA foreign_key_check').fetchall(), [])
            self.assertEqual(db.execute('SELECT count(*) FROM operations').fetchone()[0], 8)

    def test_alternatives_stop_and_recover_without_calendar_completion(self):
        with TestClient(create_app(self.path)) as client:
            for skill in list(EXERCISES)[1:]:
                for status in ('stopped', 'interrupted'):
                    create = self.create_body(skill)
                    client.post('/api/sessions', json=create)
                    url = '/api/sessions/' + create['session_id']
                    checkpoint = dict(operation_id=str(uuid4()), owner_token=create['owner_token'], expected_revision=1,
                                      status='in_progress', active_duration_ms=12345, paused_duration_ms=1000, ended_at=None)
                    self.assertEqual(client.put(url, json=checkpoint).status_code, 200)
                    final = checkpoint | dict(operation_id=str(uuid4()), expected_revision=2, status=status,
                                              ended_at='2026-11-02T12:00:20Z')
                    result = client.put(url, json=final)
                    self.assertEqual(result.status_code, 200)
                    self.assertEqual(result.json()['session']['active_duration_ms'], 12345)
            self.assertEqual(events(self.path, '2026-11', 'UTC', 0, 100)['events'], [])

    def test_old_rows_and_operation_receipts_survive_migration_twice(self):
        with patch('backend.app.db.migrate_exercises'):
            initialize(self.path, True)
        body = self.create_body('paced_breathing_4_6')
        sessions.create(self.path, SessionCreate(**body))
        def snapshot():
            with connect(self.path) as db:
                return {table: [tuple(row) for row in db.execute('SELECT * FROM ' + table)]
                        for table in ('exercise_sessions', 'operations', 'demo_users')}
        before = snapshot()
        initialize(self.path, True)
        initialize(self.path, True)
        self.assertEqual(snapshot(), before)
        self.assertTrue(sessions.create(self.path, SessionCreate(**body))['replayed'])
        with connect(self.path) as db:
            self.assertEqual(db.execute('PRAGMA foreign_key_check').fetchall(), [])
            self.assertEqual(db.execute('SELECT count(*) FROM schema_migrations WHERE version=8').fetchone()[0], 1)

    def test_grounding_can_finish_early_and_replay_actual_duration(self):
        with TestClient(create_app(self.path)) as client:
            create = self.create_body('sensory_grounding_5_4_3_2_1')
            client.post('/api/sessions', json=create)
            final = dict(operation_id=str(uuid4()), owner_token=create['owner_token'], expected_revision=1,
                         status='completed', active_duration_ms=12345, paused_duration_ms=0,
                         ended_at='2026-11-02T12:00:13Z')
            url = '/api/sessions/' + create['session_id']
            self.assertEqual(client.put(url, json=final).status_code, 200)
            self.assertTrue(client.put(url, json=final).json()['replayed'])
            self.assertEqual(client.get(url).json()['session']['active_duration_ms'], 12345)
