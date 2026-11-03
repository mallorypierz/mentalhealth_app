from typing import Literal
from uuid import UUID
from pydantic import AwareDatetime, BaseModel, ConfigDict
from .exercises import SkillKey


class SessionCreate(BaseModel):
    model_config = ConfigDict(extra='forbid')
    session_id: UUID
    operation_id: UUID
    skill_key: SkillKey
    started_at: AwareDatetime
    owner_token: UUID | None = None


class SessionRecord(BaseModel):
    id: UUID
    skill_key: SkillKey
    status: Literal['in_progress', 'completed', 'stopped', 'interrupted']
    started_at: AwareDatetime
    ended_at: AwareDatetime | None
    active_duration_ms: int
    paused_duration_ms: int
    last_checkpoint_at: AwareDatetime
    revision: int
    is_fixture: bool


class SessionResult(BaseModel):
    session: SessionRecord
    persistence: Literal['saved'] = 'saved'
    replayed: bool = False


from pydantic import Field, model_validator


class SessionUpdate(BaseModel):
    model_config = ConfigDict(extra='forbid')
    operation_id: UUID
    owner_token: UUID
    expected_revision: int = Field(ge=1)
    status: Literal['in_progress', 'completed', 'stopped', 'interrupted']
    active_duration_ms: int = Field(ge=0, le=75000, strict=True)
    paused_duration_ms: int = Field(ge=0, strict=True)
    ended_at: AwareDatetime | None = None

    @model_validator(mode='after')
    def consistent(self):
        if (self.status == 'in_progress') != (self.ended_at is None):
            raise ValueError('Terminal sessions require an end time.')
        return self


class SessionList(BaseModel):
    sessions: list[SessionRecord]
    next_cursor: int | None
