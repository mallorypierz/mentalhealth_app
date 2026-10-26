import hashlib
from dataclasses import dataclass
from contextvars import ContextVar
from .db import DEMO_USER_ID


class IdentityError(Exception):
    def __init__(self, status, code, message):
        self.status, self.code, self.message = status, code, message
        super().__init__(message)


@dataclass(frozen=True)
class Identity:
    session_id: str
    owner_id: str | None
    version: int
    kind: str = 'chooser'
    display_name: str | None = None


def token_hash(authorization):
    # Do not put the supplied header/token in exceptions or logs.
    if not authorization or not authorization.startswith('Bearer '):
        raise IdentityError(401, 'identity_required', 'Choose a local profile first.')
    token = authorization[7:]
    if not 40 <= len(token) <= 128:
        raise IdentityError(401, 'identity_required', 'Local access is invalid or revoked.')
    return hashlib.sha256(token.encode()).hexdigest()


def resolve(db, authorization):
    row = db.execute('SELECT b.id,b.active_owner_id,b.context_version,u.kind,u.display_name '
                     'FROM browser_sessions b LEFT JOIN demo_users u ON u.id=b.active_owner_id '
                     'WHERE token_hash=? AND revoked_at IS NULL', (token_hash(authorization),)).fetchone()
    if row is None:
        raise IdentityError(401, 'identity_required', 'Local access is invalid or revoked.')
    return Identity(row['id'], row['active_owner_id'], row['context_version'],
                    row['kind'] or 'chooser', row['display_name'])


# Each request/background task gets its own immutable context; never a global owner.
active_context = ContextVar('active_identity', default=None)


def owner():
    identity = active_context.get()
    return identity.owner_id if identity else DEMO_USER_ID


def validate_context(db):
    identity = active_context.get()
    if identity is None:  # Preserved single-owner test/Part 2 factory mode only.
        return
    row = db.execute('SELECT active_owner_id,context_version,revoked_at FROM browser_sessions WHERE id=?',
                     (identity.session_id,)).fetchone()
    if not row or row['revoked_at'] or (row['active_owner_id'], row['context_version']) != (identity.owner_id, identity.version):
        raise IdentityError(409, 'stale_context', 'Profile context changed. Reload before continuing.')
    if not identity.owner_id:
        raise IdentityError(401, 'identity_required', 'Continue as guest or choose a local profile.')
