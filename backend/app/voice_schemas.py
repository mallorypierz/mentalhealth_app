from typing import Literal
from uuid import UUID
from pydantic import Field
from .chat_schemas import Input

class VoiceSessionCreate(Input):
    session_id: UUID
    conversation_id: UUID
    operation_id: UUID

class VoiceAction(Input):
    operation_id: UUID
    expected_revision: int = Field(ge=1)
    action: Literal['cancel', 'retry_speech', 'retry_reply_save'] = 'cancel'

class VoiceStop(Input):
    operation_id: UUID
    expected_revision: int = Field(ge=1)

class MockTurn(Input):
    type: Literal['mock_turn']
    turn_id: UUID
    request_id: UUID
    operation_id: UUID
    # Deterministic test cases, not user-selected model or provider settings.
    scenario: Literal['success', 'transcription_failure', 'model_failure', 'speech_failure', 'delayed'] = 'success'


class AudioTurn(Input):
    type: Literal['audio_turn']
    turn_id: UUID
    request_id: UUID
    operation_id: UUID
    audio: str = Field(min_length=60, max_length=1280060)
