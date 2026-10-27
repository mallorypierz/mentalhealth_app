import tempfile
import unittest
from pathlib import Path
from uuid import uuid4
from dataclasses import replace
from concurrent.futures import ThreadPoolExecutor
from backend.app.db import initialize,connect
from backend.app.config import Settings
from backend.app.repositories import voice_budget as budget
from backend.app.repositories.provider_usage import LimitError

class TestingSessions(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.path=Path(self.tmp.name)/'test.sqlite3';initialize(self.path,True)
        self.id=str(uuid4())
        self.settings=Settings(api_key='offline-test',voice_enabled=True,voice_prices_verified=True,voice_test_session_id=self.id)
    def tearDown(self): self.tmp.cleanup()
    def test_old_calls_remain_unassigned_and_new_session_survives_restart(self):
        with connect(self.path) as db:
            db.execute("INSERT INTO voice_provider_attempts VALUES ('old','old','speech',50000,'failed','2026-10-27',NULL)")
        budget.create_test_session(self.path,self.id,'Student demo',50,2500000)
        budget.reserve(self.path,'first','transcription',self.settings)
        initialize(self.path,True)
        budget.create_test_session(self.path,self.id,'Student demo',50,2500000)
        self.assertEqual(budget.status(self.path,self.settings)['used'],1)
        with connect(self.path) as db:
            self.assertEqual(db.execute('SELECT COUNT(*) FROM voice_provider_attempts').fetchone()[0],2)
            self.assertIsNone(db.execute("SELECT test_session_id FROM voice_provider_attempts WHERE id='old'").fetchone()[0])
        with self.assertRaises(ValueError):budget.create_test_session(self.path,str(uuid4()),'Another',50,2500000)
    def test_fifty_atomic_attempts_then_mock_without_reset(self):
        budget.create_test_session(self.path,self.id,'Offline cap test',50,2500000)
        def reserve(i):
            try:
                ident=budget.reserve(self.path,str(i),'planning',self.settings)
                budget.finish(self.path,ident,'failed');return 1
            except LimitError:return 0
        with ThreadPoolExecutor(max_workers=8) as pool:self.assertEqual(sum(pool.map(reserve,range(60))),50)
        self.assertEqual(budget.effective_settings(self.path,self.settings).provider,'mock')
        initialize(self.path,True)
        self.assertEqual(budget.status(self.path,self.settings)['remaining'],0)
        with self.assertRaises(LimitError):budget.reserve(self.path,'again','speech',self.settings)
    def test_closed_unknown_and_spending_limit(self):
        self.assertEqual(budget.effective_settings(self.path,self.settings).provider,'mock')
        budget.create_test_session(self.path,self.id,'Low budget',50,50000)
        budget.reserve(self.path,'only','answer',self.settings)
        self.assertEqual(budget.status(self.path,self.settings)['remaining'],0)
        budget.close_test_session(self.path,self.id)
        nextid=str(uuid4());budget.create_test_session(self.path,nextid,'Explicit next',10,500000)
        self.assertEqual(budget.status(self.path,replace(self.settings,voice_test_session_id=nextid))['used'],0)
        self.assertEqual(budget.effective_settings(self.path,self.settings).provider,'mock')
        with self.assertRaises(ValueError):budget.create_test_session(self.path,str(uuid4()),'Invalid',51,2500000)
