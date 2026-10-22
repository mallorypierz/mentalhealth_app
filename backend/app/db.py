from pathlib import Path
import sqlite3

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATABASE_PATH = PROJECT_ROOT / 'data' / 'app.sqlite3'
DEMO_USER_ID = '00000000-0000-4000-8000-000000000001'


def connect(path: Path):
    db = sqlite3.connect(path, timeout=5)
    db.row_factory = sqlite3.Row
    db.execute('PRAGMA foreign_keys = ON')
    return db


def initialize(path: Path):
    path.parent.mkdir(parents=True, exist_ok=True)
    db = connect(path)
    try:
        db.executescript((Path(__file__).parent / 'migrations' / '001_initial.sql').read_text())
        db.executescript((Path(__file__).parent / 'migrations' / '002_conversations.sql').read_text())
        db.executescript((Path(__file__).parent / 'migrations' / '003_provider_usage.sql').read_text())
        columns = {row[1] for row in db.execute("PRAGMA table_info(exercise_sessions)")}
        if "owner_token" not in columns:
            db.execute("ALTER TABLE exercise_sessions ADD COLUMN owner_token TEXT")
        request_columns = {row[1] for row in db.execute("PRAGMA table_info(requests)")}
        for name, definition in {
            'retrieval_outcome': "TEXT NOT NULL DEFAULT 'not_run'",
            'retrieved_ids_json': "TEXT NOT NULL DEFAULT '[]'",
            'citations_json': "TEXT NOT NULL DEFAULT '[]'",
            'failure_stage': 'TEXT',
            'provider': "TEXT NOT NULL DEFAULT 'mock'",
            'model': 'TEXT',
        }.items():
            if name not in request_columns:
                db.execute(f'ALTER TABLE requests ADD COLUMN {name} {definition}')
        with db:
            db.execute('INSERT OR IGNORE INTO demo_users(id, display_name) VALUES (?, ?)',
                       (DEMO_USER_ID, 'Fictional coursework student'))
    finally:
        db.close()
