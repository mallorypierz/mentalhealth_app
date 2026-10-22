from contextlib import asynccontextmanager
from pathlib import Path
from uuid import UUID
import sqlite3
import asyncio
from .api.conversations import router as conversation_router
from .repositories import conversations
from fastapi import FastAPI, Request, Response, Query
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from .db import DATABASE_PATH, initialize
from .config import Settings, load
from .repositories import provider_usage
from .schemas import SessionCreate, SessionResult, SessionUpdate, SessionList
from .repositories import sessions


def error(status, code, message, retryable=False, persistence='not_saved'):
    return JSONResponse(status_code=status, content={
        'error': {'code': code, 'message': message, 'retryable': retryable},
        'persistence': persistence,
    })


def create_app(database_path: Path = DATABASE_PATH, settings=None):
    settings = settings or Settings()
    tasks = set()
    @asynccontextmanager
    async def lifespan(app):
        initialize(database_path)
        conversations.recover_pending(database_path)
        yield
        for task in list(tasks):
            task.cancel()
        if tasks:
            await asyncio.gather(*list(tasks), return_exceptions=True)

    app = FastAPI(title='Coursework session API', lifespan=lifespan)

    app.include_router(conversation_router(database_path, tasks, settings))

    @app.get('/api/health')
    def health():
        used = provider_usage.used(database_path)
        return {'provider': settings.provider, 'model': settings.model if settings.provider == 'openai' else None,
                'configured': not settings.error and (settings.provider == 'mock' or bool(settings.api_key)),
                'live_calls_used': used, 'live_call_limit': settings.call_limit,
                'live_calls_remaining': max(0, settings.call_limit-used)}

    @app.exception_handler(conversations.NotFound)
    async def not_found(request: Request, exc):
        return error(404, 'not_found', str(exc))

    @app.exception_handler(conversations.Conflict)
    async def conflict(request: Request, exc):
        return error(409, 'operation_conflict', str(exc))

    @app.exception_handler(RequestValidationError)
    async def validation_error(request: Request, exc):
        return error(422, 'invalid_input', 'Check the identifiers, message length, mode, skill, durations, status, and timezone-aware times.')

    @app.exception_handler(sqlite3.Error)
    async def database_error(request: Request, exc):
        return error(503, 'database_unavailable', 'The database operation could not be completed.',
                     True, 'unknown')

    @app.post('/api/sessions', response_model=SessionResult, status_code=201)
    def create_session(body: SessionCreate, response: Response):
        try:
            result = sessions.create(database_path, body)
        except sessions.Conflict as exc:
            return error(409, 'operation_conflict', str(exc))
        if result['replayed']:
            response.status_code = 200
        return result

    @app.get('/api/sessions', response_model=SessionList)
    def list_sessions(cursor: int = Query(0, ge=0), limit: int = Query(20, ge=1, le=100)):
        return sessions.list_sessions(database_path, cursor, limit)

    @app.put('/api/sessions/{session_id}', response_model=SessionResult)
    def update_session(session_id: UUID, body: SessionUpdate):
        try:
            result = sessions.update(database_path, session_id, body)
        except sessions.Conflict as exc:
            return error(409, 'operation_conflict', str(exc))
        if result is None:
            return error(404, 'session_not_found', 'Session not found.')
        return result

    @app.get('/api/sessions/{session_id}', response_model=SessionResult)
    def get_session(session_id: UUID):
        record = sessions.get(database_path, session_id)
        if record is None:
            return error(404, 'session_not_found', 'Session not found.')
        return {'session': record, 'persistence': 'saved', 'replayed': False}

    return app


app = create_app(settings=load())
