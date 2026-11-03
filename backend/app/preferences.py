"""Profile-scoped opt-in preferences. No history inference or provider access."""
import hashlib
import json
from typing import Literal
from uuid import UUID
from fastapi import APIRouter
from pydantic import BaseModel, ConfigDict, Field
from .db import connect
from .identity import active_context, owner, validate_context, IdentityError

class Answers(BaseModel):
    model_config = ConfigDict(extra='forbid')
    activity: Literal['', 'none', 'paced_breathing_4_6', 'sensory_grounding_5_4_3_2_1', 'stop', 'cognitive_reframe']
    breath: Literal['', 'none', 'yes', 'avoid', 'unsure']

class Change(BaseModel):
    model_config = ConfigDict(extra='forbid')
    operation_id: UUID
    expected_revision: int = Field(ge=0)
    answers: Answers | None  # null explicitly forgets; no implicit saves

class Result(BaseModel):
    id: str
    revision: int
    answers: Answers | None
    persistence: Literal['saved'] = 'saved'
    replayed: bool = False


def record(db):
    row = db.execute('SELECT revision,answers FROM preferences WHERE owner_id=?', (owner(),)).fetchone()
    return dict(id=owner(), revision=row['revision'] if row else 0,
                answers=json.loads(row['answers']) if row and row['answers'] else None)


def router(path):
    api = APIRouter(prefix='/api/preferences')
    @api.get('', response_model=Result)
    def read():
        with connect(path) as db:
            validate_context(db)
            return record(db)

    @api.put('', response_model=Result)
    def write(body: Change):
        fingerprint = hashlib.sha256(json.dumps(body.model_dump(mode='json', exclude={'operation_id'}), sort_keys=True).encode()).hexdigest()
        with connect(path) as db:
            db.execute('BEGIN IMMEDIATE')
            validate_context(db)
            if active_context.get().kind != 'profile':
                raise IdentityError(422, 'profile_required', 'Guest quiz answers are temporary. Choose a profile to remember preferences.')
            old = db.execute('SELECT fingerprint FROM preference_operations WHERE owner_id=? AND operation_id=?', (owner(),str(body.operation_id))).fetchone()
            if old:
                if old['fingerprint'] != fingerprint:
                    raise IdentityError(409,'operation_conflict','Retry the original preference operation.')
                return record(db) | {'replayed': True}
            current = record(db)
            if current['revision'] != body.expected_revision:
                raise IdentityError(409,'revision_conflict','Saved preferences changed. Reload before saving again.')
            db.execute('INSERT INTO preferences VALUES (?,?,?) ON CONFLICT(owner_id) DO UPDATE SET revision=excluded.revision,answers=excluded.answers',
                       (owner(), current['revision']+1, body.answers.model_dump_json() if body.answers else None))
            db.execute('INSERT INTO preference_operations VALUES (?,?,?)', (owner(),str(body.operation_id),fingerprint))
            return record(db)
    return api
