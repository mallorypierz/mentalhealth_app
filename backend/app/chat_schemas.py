from typing import Literal
from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field, AwareDatetime, field_validator

MockMode = Literal['success', 'failure', 'delayed']

class Input(BaseModel):
    model_config = ConfigDict(extra='forbid')

class ConversationCreate(Input):
    conversation_id: UUID
    operation_id: UUID

class MessageSubmit(Input):
    request_id: UUID
    content: str = Field(min_length=1, max_length=2000)
    mock_mode: MockMode = 'success'

    @field_validator('content')
    @classmethod
    def nonblank(cls, value):
        if not value.strip():
            raise ValueError('Message cannot be blank.')
        return value

class RetryRequest(Input):
    operation_id: UUID
    mock_mode: MockMode = 'success'

class Conversation(BaseModel):
    id: UUID
    created_at: AwareDatetime
    updated_at: AwareDatetime

class ConversationPage(BaseModel):
    conversations: list[Conversation]
    next_cursor: int | None

class Message(BaseModel):
    id: UUID
    conversation_id: UUID
    request_id: UUID
    provider: str = 'mock'
    model: str | None = None
    role: Literal['user', 'assistant']
    content: str
    sequence: int
    created_at: AwareDatetime
    request_status: Literal['pending', 'succeeded', 'failed']
    error_code: str | None

class MessagePage(BaseModel):
    latest_request_id: UUID | None
    messages: list[Message]
    next_cursor: int | None

class RequestStatus(BaseModel):
    id: UUID
    conversation_id: UUID
    status: Literal['pending', 'succeeded', 'failed']
    attempt_count: int
    provider_call_count: int
    error_code: str | None
    user_message_id: UUID
    assistant_message_id: UUID | None
    assistant_content: str | None
    created_at: AwareDatetime
    updated_at: AwareDatetime
    retrieval_outcome: str
    retrieved_record_ids: list[str]
    citations: list[str]
    failure_stage: str | None
    provider: str = 'mock'
    model: str | None = None
    user_persistence: Literal['saved'] = 'saved'
    assistant_persistence: Literal['saved', 'not_saved']
