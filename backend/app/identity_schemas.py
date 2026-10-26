from typing import Literal
from uuid import UUID

from pydantic import AwareDatetime, BaseModel, ConfigDict, Field, field_validator


class Input(BaseModel):
    model_config = ConfigDict(extra='forbid')


class Bootstrap(Input):
    bootstrap_id: UUID


class ProfileCreate(Input):
    profile_id: UUID
    operation_id: UUID
    display_name: str = Field(min_length=1, max_length=60)
    age: int | None = Field(default=None, ge=0, le=120, strict=True)
    gender: str | None = Field(default=None, max_length=60)

    @field_validator('display_name')
    @classmethod
    def name(cls, value):
        value = value.strip()
        if not value or any(ord(c) < 32 for c in value):
            raise ValueError('Use a nonblank display name without control characters.')
        return value

    @field_validator('gender')
    @classmethod
    def optional_gender(cls, value):
        if value is None:
            return None
        value = value.strip()
        if any(ord(c) < 32 for c in value):
            raise ValueError('Control characters are not allowed.')
        return value or None


class ProfileSelect(Input):
    profile_id: UUID
    operation_id: UUID
    expected_context_version: int = Field(ge=1, strict=True)
    guest_disposition: Literal['save', 'discard'] | None = None


class IdentityAction(Input):
    operation_id: UUID
    expected_context_version: int = Field(ge=1, strict=True)
    confirm_discard: bool = False


class ProfileDelete(IdentityAction):
    expected_revision: int = Field(ge=1, strict=True)
    confirm_delete: Literal[True]


class ProfileEdit(Input):
    operation_id: UUID
    expected_revision: int = Field(ge=1, strict=True)
    display_name: str = Field(min_length=1, max_length=60)
    age: int | None = Field(default=None, ge=0, le=120, strict=True)
    gender: str | None = Field(default=None, max_length=60)

    _name = field_validator('display_name')(ProfileCreate.name.__func__)
    _gender = field_validator('gender')(ProfileCreate.optional_gender.__func__)


class Profile(BaseModel):
    id: UUID
    display_name: str
    age: int | None
    gender: str | None
    kind: Literal['profile']
    created_at: AwareDatetime
    updated_at: AwareDatetime
    revision: int


class ProfileResult(BaseModel):
    profile: Profile
    persistence: Literal['saved'] = 'saved'
    replayed: bool = False


class ProfileSummary(BaseModel):
    id: UUID
    display_name: str
    created_at: AwareDatetime


class ProfileList(BaseModel):
    profiles: list[ProfileSummary]


class IdentityResult(BaseModel):
    browser_session_id: UUID
    active_owner_id: UUID | None
    context_version: int
    mode: Literal['chooser', 'profile', 'guest']
    display_name: str | None = None
    authentication: Literal['local_chooser_not_authentication'] = 'local_chooser_not_authentication'
    replayed: bool = False


class BootstrapResult(IdentityResult):
    access_token: str
    token_type: Literal['Bearer'] = 'Bearer'
