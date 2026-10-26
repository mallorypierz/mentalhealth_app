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


def initialize(path: Path, enable_profiles=False):
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
        if enable_profiles:
            migrate_identities(db)
    finally:
        db.close()


def migrate_identities(db):
    # Unlike executescript, execute preserves the enclosing transaction. Serialize
    # the version check and all DDL so a partial migration can be rolled back.
    with db:
        db.execute('BEGIN IMMEDIATE')
        db.execute('CREATE TABLE IF NOT EXISTS schema_migrations(version INTEGER PRIMARY KEY)')
        if db.execute('SELECT 1 FROM schema_migrations WHERE version=4').fetchone():
            return
        source = (Path(__file__).parent / 'migrations' / '004_identities.sql').read_text()
        statement = ''
        for line in source.splitlines(keepends=True):
            statement += line
            if sqlite3.complete_statement(statement):
                db.execute(statement)
                statement = ''
        if statement.strip():
            raise ValueError('Incomplete identity migration.')
        db.execute('INSERT INTO schema_migrations(version) VALUES (4)')
