"""Audit-only mock failure injection; no credentials loaded or provider calls."""
from pathlib import Path
from backend.app.main import create_app
from backend.app.providers import mock
from backend.app.config import Settings
original_plan = mock.plan
async def failing_plan(question, schema, mode):
    if Path('/tmp/mentalhealth-final-failure').exists():
        raise mock.MockFailure('Deliberate final-audit mock planning failure')
    return await original_plan(question,schema,mode)
mock.plan = failing_plan
app=create_app(Path(__file__).parent/'data/app.sqlite3',settings=Settings(),enable_profiles=True)
