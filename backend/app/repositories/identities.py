import hashlib
import json
import secrets
from uuid import uuid4
from contextlib import contextmanager
from datetime import datetime, timezone

from ..db import connect
from ..identity import IdentityError, resolve


def now():
    return datetime.now(timezone.utc).isoformat()


@contextmanager
def connection(path, write=False):
    db = connect(path)
    try:
        with db:
            if write:
                db.execute('BEGIN IMMEDIATE')
            yield db
    finally:
        db.close()


def identity_result(identity, replayed=False):
    return dict(browser_session_id=identity.session_id, active_owner_id=identity.owner_id,
                context_version=identity.version, mode=identity.kind, display_name=identity.display_name,
                replayed=replayed)


def bootstrap(path, body):
    token = secrets.token_urlsafe(32)
    with connection(path, True) as db:
        if db.execute('SELECT 1 FROM browser_sessions WHERE id=?', (str(body.bootstrap_id),)).fetchone():
            # Never disclose an existing token or reset an existing session using a public UUID.
            raise IdentityError(409, 'bootstrap_exists', 'Start a new chooser session with a new bootstrap ID.')
        db.execute('INSERT INTO browser_sessions(id,token_hash,created_at) VALUES (?,?,?)',
                   (str(body.bootstrap_id), hashlib.sha256(token.encode()).hexdigest(), now()))
        result = identity_result(resolve(db, 'Bearer ' + token))
    return result | {'access_token': token}


def read_identity(path, authorization):
    with connection(path) as db:
        return identity_result(resolve(db, authorization))


def profile_row(db, profile_id):
    row = db.execute("SELECT id,display_name,age,gender,kind,created_at,updated_at,revision "
                     "FROM demo_users WHERE id=? AND kind='profile'", (str(profile_id),)).fetchone()
    if row is None:
        raise IdentityError(404, 'not_found', 'Profile not found.')
    return dict(row)


def operation(db, identity, body, kind):
    digest = hashlib.sha256(json.dumps(body.model_dump(mode='json'), sort_keys=True).encode()).hexdigest()
    old = db.execute('SELECT * FROM identity_operations WHERE id=?', (str(body.operation_id),)).fetchone()
    if old and (old['browser_session_id'], old['operation_type'], old['input_hash']) != (identity.session_id, kind, digest):
        raise IdentityError(409, 'operation_conflict', 'Operation ID was reused with different input or access.')
    return old, digest


def save_operation(db, identity, body, kind, digest, version, target=None):
    db.execute('INSERT INTO identity_operations VALUES (?,?,?,?,?,?)',
               (str(body.operation_id), identity.session_id, kind, digest,
                str(target if target is not None else body.profile_id), version))


def create(path, authorization, body):
    with connection(path, True) as db:
        identity = resolve(db, authorization)
        old, digest = operation(db, identity, body, 'create_profile')
        if old:
            return {'profile': profile_row(db, old['result_id']), 'replayed': True}
        if db.execute('SELECT id FROM demo_users WHERE id=? UNION SELECT id FROM deleted_identities WHERE id=?',
                      (str(body.profile_id), str(body.profile_id))).fetchone():
            raise IdentityError(409, 'profile_exists', 'That profile ID already exists; retry the original operation.')
        stamp = now()
        db.execute("INSERT INTO demo_users(id,display_name,kind,age,gender,created_at,updated_at) "
                   "VALUES (?,?,'profile',?,?,?,?)", (str(body.profile_id), body.display_name, body.age, body.gender, stamp, stamp))
        save_operation(db, identity, body, 'create_profile', digest, identity.version)
        return {'profile': profile_row(db, body.profile_id), 'replayed': False}


def listing(path, authorization):
    with connection(path) as db:
        resolve(db, authorization)
        # The explicitly shared local chooser exposes names, not demographic/activity details.
        return {'profiles': [dict(r) for r in db.execute(
            "SELECT id,display_name,created_at FROM demo_users WHERE kind='profile' ORDER BY created_at,id")]}


def select(path, authorization, body):
    with connection(path, True) as db:
        identity = resolve(db, authorization)
        old, digest = operation(db, identity, body, 'select_profile')
        if old:
            if identity.version != old['context_version'] or identity.owner_id != old['result_id']:
                raise IdentityError(409, 'stale_context', 'This selection belongs to an older context.')
            return identity_result(identity, True)
        if identity.version != body.expected_context_version:
            raise IdentityError(409, 'stale_context', 'Refresh the current profile context.')
        require_idle(db, identity.owner_id)
        profile_row(db, body.profile_id)
        if identity.kind == 'guest':
            if body.guest_disposition is None:
                raise IdentityError(409, 'guest_choice_required', 'Choose Save and switch, Discard and switch, or Cancel.')
            if body.guest_disposition == 'save':
                for table in ('exercise_sessions', 'conversations', 'operations', 'conversation_operations'):
                    db.execute('UPDATE ' + table + ' SET demo_user_id=? WHERE demo_user_id=?',
                               (str(body.profile_id), identity.owner_id))
            else:
                delete_activity(db, identity.owner_id)
            db.execute('UPDATE browser_sessions SET active_owner_id=NULL,context_version=context_version+1 '
                       'WHERE active_owner_id=? AND id<>?', (identity.owner_id, identity.session_id))
            db.execute('UPDATE browser_sessions SET active_owner_id=NULL WHERE id=?', (identity.session_id,))
            db.execute('INSERT INTO deleted_identities VALUES (?)', (identity.owner_id,))
            db.execute('DELETE FROM demo_users WHERE id=?', (identity.owner_id,))
        db.execute('UPDATE browser_sessions SET active_owner_id=?,context_version=context_version+1 WHERE id=?',
                   (str(body.profile_id), identity.session_id))
        save_operation(db, identity, body, 'select_profile', digest, identity.version + 1)
        return identity_result(resolve(db, authorization))


def read_profile(path, authorization):
    with connection(path) as db:
        identity = resolve(db, authorization)
        if identity.owner_id is None:
            raise IdentityError(409, 'profile_not_selected', 'Choose a profile to view its details.')
        return {'profile': profile_row(db, identity.owner_id), 'replayed': False}


def require_idle(db, owner_id):
    if not owner_id:
        return
    pending = db.execute("SELECT 1 FROM requests r JOIN conversations c ON c.id=r.conversation_id "
                         "WHERE c.demo_user_id=? AND r.status='pending'", (owner_id,)).fetchone()
    active = db.execute("SELECT 1 FROM exercise_sessions WHERE demo_user_id=? AND status='in_progress'",
                        (owner_id,)).fetchone()
    if pending or active:
        raise IdentityError(409, 'work_in_progress', 'Finish or stop practice and wait for pending saves/replies before switching.')


def replay_action(db, identity, body, kind):
    old, digest = operation(db, identity, body, kind)
    if old:
        if identity.version != old['context_version']:
            raise IdentityError(409, 'stale_context', 'This operation belongs to an older context.')
        return identity_result(identity, True), digest
    if identity.version != body.expected_context_version:
        raise IdentityError(409, 'stale_context', 'Refresh the current profile context.')
    return None, digest


def guest(path, authorization, body):
    with connection(path, True) as db:
        identity = resolve(db, authorization)
        replay, digest = replay_action(db, identity, body, 'guest')
        if replay:
            return replay
        if identity.owner_id:
            raise IdentityError(409, 'leave_first', 'Leave the current visit before starting another guest visit.')
        guest_id, stamp = str(uuid4()), now()
        db.execute("INSERT INTO demo_users(id,display_name,kind,created_at,updated_at) VALUES (?,'Guest','guest',?,?)",
                   (guest_id, stamp, stamp))
        db.execute('UPDATE browser_sessions SET active_owner_id=?,context_version=context_version+1 WHERE id=?',
                   (guest_id, identity.session_id))
        save_operation(db, identity, body, 'guest', digest, identity.version+1, guest_id)
        return identity_result(resolve(db, authorization))


def delete_activity(db, owner_id):
    # Paid-call evidence is retained, never deleted to reset a budget. New identities are mock-only.
    if db.execute('SELECT 1 FROM provider_attempts p JOIN requests r ON r.id=p.request_id '
                  'JOIN conversations c ON c.id=r.conversation_id WHERE c.demo_user_id=?', (owner_id,)).fetchone():
        raise IdentityError(409, 'protected_evidence', 'Historical provider evidence cannot be deleted here.')
    db.execute('DELETE FROM messages WHERE conversation_id IN (SELECT id FROM conversations WHERE demo_user_id=?)', (owner_id,))
    db.execute('DELETE FROM requests WHERE conversation_id IN (SELECT id FROM conversations WHERE demo_user_id=?)', (owner_id,))
    db.execute('DELETE FROM conversation_operations WHERE demo_user_id=?', (owner_id,))
    db.execute('DELETE FROM conversations WHERE demo_user_id=?', (owner_id,))
    db.execute('DELETE FROM operations WHERE demo_user_id=?', (owner_id,))
    db.execute('DELETE FROM exercise_sessions WHERE demo_user_id=?', (owner_id,))


def leave(path, authorization, body, delete=False):
    with connection(path, True) as db:
        identity = resolve(db, authorization)
        kind = 'delete_profile' if delete else 'leave'
        replay, digest = replay_action(db, identity, body, kind)
        if replay:
            return replay
        require_idle(db, identity.owner_id)
        if delete:
            profile = profile_row(db, identity.owner_id)
            if profile['revision'] != body.expected_revision:
                raise IdentityError(409, 'stale_revision', 'Profile changed. Read it before deleting.')
        if identity.kind == 'guest' and not body.confirm_discard:
            raise IdentityError(409, 'guest_choice_required', 'Confirm discarding this guest activity.')
        remove = delete or identity.kind == 'guest'
        if remove:
            delete_activity(db, identity.owner_id)
            # Other sessions lose access; this session remains a chooser so a lost deletion response is retryable.
            db.execute('UPDATE browser_sessions SET active_owner_id=NULL,context_version=context_version+1,revoked_at=? '
                       'WHERE active_owner_id=? AND id<>?', (now(), identity.owner_id, identity.session_id))
            db.execute('DELETE FROM identity_operations WHERE result_id=?', (identity.owner_id,))
        db.execute('UPDATE browser_sessions SET active_owner_id=NULL,context_version=context_version+1 WHERE id=?', (identity.session_id,))
        if remove:
            db.execute('INSERT INTO deleted_identities VALUES (?)', (identity.owner_id,))
            db.execute('DELETE FROM demo_users WHERE id=?', (identity.owner_id,))
        save_operation(db, identity, body, kind, digest, identity.version+1, identity.owner_id or '')
        return identity_result(resolve(db, authorization))


def edit(path, authorization, body):
    with connection(path, True) as db:
        identity = resolve(db, authorization)
        old, digest = operation(db, identity, body, 'edit_profile')
        profile = profile_row(db, identity.owner_id)
        if old:
            if old['result_id'] != identity.owner_id:
                raise IdentityError(409, 'stale_context', 'This edit belongs to another profile.')
            return {'profile': profile, 'replayed': True}
        if profile['revision'] != body.expected_revision:
            raise IdentityError(409, 'stale_revision', 'Profile changed. Read it before editing.')
        db.execute('UPDATE demo_users SET display_name=?,age=?,gender=?,updated_at=?,revision=revision+1 WHERE id=?',
                   (body.display_name, body.age, body.gender, now(), identity.owner_id))
        save_operation(db, identity, body, 'edit_profile', digest, identity.version, identity.owner_id)
        return {'profile': profile_row(db, identity.owner_id), 'replayed': False}
