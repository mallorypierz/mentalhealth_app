import hashlib
import json
from datetime import datetime, timezone
from ..db import connect, DEMO_USER_ID


class Conflict(Exception):
    pass


def public_record(row):
    record = dict(row)
    record.pop('demo_user_id', None)
    record.pop('owner_token', None)
    record['is_fixture'] = bool(record['is_fixture'])
    return record


def create(path, request):
    payload = request.model_dump(mode='json', exclude={'operation_id'})
    payload['started_at'] = request.started_at.astimezone(timezone.utc).isoformat()
    fingerprint = hashlib.sha256(json.dumps(payload, sort_keys=True).encode()).hexdigest()
    db = connect(path)
    try:
        with db:
            # Acquire the write lock before checking duplicates: concurrent callers
            # cannot both pass the check and create separate operation results.
            db.execute('BEGIN IMMEDIATE')
            existing = db.execute('SELECT * FROM operations WHERE id = ?',
                                  (str(request.operation_id),)).fetchone()
            if existing:
                if (existing['demo_user_id'] != DEMO_USER_ID or
                        existing['operation_type'] != 'create_session' or
                        existing['input_hash'] != fingerprint):
                    raise Conflict('Operation ID was already used with different input.')
                return {'session': json.loads(existing['result_json']), 'persistence': 'saved', 'replayed': True}
            if db.execute('SELECT 1 FROM exercise_sessions WHERE id = ?',
                          (str(request.session_id),)).fetchone():
                raise Conflict('Session ID already exists. Retry with the original operation ID.')
            db.execute('''INSERT INTO exercise_sessions
                (id, demo_user_id, skill_key, status, started_at, last_checkpoint_at, owner_token)
                VALUES (?, ?, ?, ?, ?, ?, ?)''',
                (str(request.session_id), DEMO_USER_ID, request.skill_key, 'in_progress',
                 payload['started_at'], datetime.now(timezone.utc).isoformat(),
                 str(request.owner_token) if request.owner_token else None))
            record = public_record(db.execute('SELECT * FROM exercise_sessions WHERE id = ?',
                                               (str(request.session_id),)).fetchone())
            db.execute('INSERT INTO operations VALUES (?, ?, ?, ?, ?, ?)',
                       (str(request.operation_id), DEMO_USER_ID, 'create_session',
                        str(request.session_id), fingerprint, json.dumps(record)))
        return {'session': record, 'persistence': 'saved', 'replayed': False}
    finally:
        db.close()


def get(path, session_id):
    db = connect(path)
    try:
        row = db.execute('SELECT * FROM exercise_sessions WHERE id = ? AND demo_user_id = ?',
                         (str(session_id), DEMO_USER_ID)).fetchone()
        return None if row is None else public_record(row)
    finally:
        db.close()


def list_sessions(path, cursor, limit):
    db = connect(path)
    try:
        rows = db.execute('SELECT * FROM exercise_sessions WHERE demo_user_id = ? ORDER BY started_at DESC, id DESC LIMIT ? OFFSET ?',
                          (DEMO_USER_ID, limit + 1, cursor)).fetchall()
        return {'sessions': [public_record(row) for row in rows[:limit]],
                'next_cursor': cursor + limit if len(rows) > limit else None}
    finally:
        db.close()


def update(path, session_id, request):
    payload = request.model_dump(mode='json', exclude={'operation_id'})
    fingerprint = hashlib.sha256(json.dumps({'id': str(session_id), **payload}, sort_keys=True).encode()).hexdigest()
    db = connect(path)
    try:
        with db:
            db.execute('BEGIN IMMEDIATE')
            row = db.execute('SELECT * FROM exercise_sessions WHERE id=? AND demo_user_id=?',
                             (str(session_id), DEMO_USER_ID)).fetchone()
            if row is None:
                return None
            if row['owner_token'] != str(request.owner_token):
                raise Conflict('This browser does not own the practice.')
            previous = db.execute('SELECT * FROM operations WHERE id=?', (str(request.operation_id),)).fetchone()
            if previous:
                if previous['input_hash'] != fingerprint or previous['operation_type'] != 'update_session':
                    raise Conflict('Operation ID was already used with different input.')
                return {'session': json.loads(previous['result_json']), 'persistence': 'saved', 'replayed': True}
            if row['status'] != 'in_progress' or row['revision'] != request.expected_revision:
                raise Conflict('Session changed. Read its saved state before retrying.')
            if request.active_duration_ms < row['active_duration_ms'] or request.paused_duration_ms < row['paused_duration_ms']:
                raise Conflict('Confirmed durations cannot decrease.')
            if request.ended_at and request.ended_at < datetime.fromisoformat(row['started_at']):
                raise Conflict('End time precedes start time.')
            if request.status == 'interrupted' and (request.active_duration_ms != row['active_duration_ms'] or request.paused_duration_ms != row['paused_duration_ms']):
                raise Conflict('Interrupted recovery must use the last saved durations.')
            db.execute('UPDATE exercise_sessions SET status=?, active_duration_ms=?, paused_duration_ms=?, ended_at=?, last_checkpoint_at=?, revision=revision+1 WHERE id=?',
                       (request.status, request.active_duration_ms, request.paused_duration_ms,
                        request.ended_at.isoformat() if request.ended_at else None,
                        datetime.now(timezone.utc).isoformat(), str(session_id)))
            record = public_record(db.execute('SELECT * FROM exercise_sessions WHERE id=?', (str(session_id),)).fetchone())
            db.execute('INSERT INTO operations VALUES (?, ?, ?, ?, ?, ?)',
                       (str(request.operation_id), DEMO_USER_ID, 'update_session', str(session_id), fingerprint, json.dumps(record)))
        return {'session': record, 'persistence': 'saved', 'replayed': False}
    finally:
        db.close()
