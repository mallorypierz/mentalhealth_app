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
from .db import DATABASE_PATH, initialize, connect
from .config import Settings, load
from .repositories import provider_usage
from .schemas import SessionCreate, SessionResult, SessionUpdate, SessionList
from .repositories import sessions
from .identity import IdentityError, resolve, active_context
from .api.identities import router as identity_router
from .calendar import router as calendar_router
from dataclasses import replace


def error(status, code, message, retryable=False, persistence='not_saved'):
    return JSONResponse(status_code=status, content={
        'error': {'code': code, 'message': message, 'retryable': retryable},
        'persistence': persistence,
    })


def create_app(database_path: Path = DATABASE_PATH, settings=None, enable_profiles=False):
    settings = settings or Settings()
    voice_settings=settings
    if enable_profiles:
        live_ready=settings.voice_enabled and settings.voice_prices_verified and bool(settings.api_key) and not settings.error
        settings = replace(settings, provider='openai' if live_ready else 'mock')
        voice_settings=settings
    tasks = set()
    @asynccontextmanager
    async def lifespan(app):
        initialize(database_path, enable_profiles=enable_profiles)
        conversations.recover_pending(database_path)
        if enable_profiles:
            from .repositories.voice import recover
            recover(database_path)
        yield
        for task in list(tasks):
            task.cancel()
        if tasks:
            await asyncio.gather(*list(tasks), return_exceptions=True)

    app = FastAPI(title='Coursework session API', lifespan=lifespan)

    app.include_router(conversation_router(database_path, tasks, settings))
    if enable_profiles:
        from .api.voice import router as voice_router
        app.include_router(voice_router(database_path, tasks, voice_settings))
        app.include_router(identity_router(database_path))
        app.include_router(calendar_router(database_path))

        @app.middleware('http')
        async def identity_scope(request, call_next):
            path = request.url.path
            protected = path == '/api/calendar' or any(path == prefix or path.startswith(prefix+'/')
                for prefix in ('/api/sessions', '/api/conversations', '/api/requests', '/api/voice'))
            token = None
            try:
                if protected:
                    db = connect(database_path)
                    try:
                        identity = resolve(db, request.headers.get('authorization'))
                    finally:
                        db.close()
                    if not identity.owner_id or identity.kind not in ('profile', 'guest'):
                        raise IdentityError(401, 'identity_required', 'Continue as guest or choose a profile.')
                    if request.headers.get('x-context-version') != str(identity.version):
                        raise IdentityError(409, 'stale_context', 'Profile context changed. Reload before continuing.')
                    token = active_context.set(identity)
                response = await call_next(request)
                if path.startswith('/api/'):
                    response.headers['Cache-Control'] = 'no-store'
                return response
            except IdentityError as exc:
                return error(exc.status, exc.code, exc.message)
            except sqlite3.Error:
                return error(503, 'database_unavailable', 'The database operation could not be completed.', True, 'unknown')
            finally:
                if token is not None:
                    active_context.reset(token)

    @app.exception_handler(IdentityError)
    async def identity_error(request: Request, exc):
        return error(exc.status, exc.code, exc.message)

    @app.get('/api/health')
    def health():
        used = provider_usage.used(database_path)
        from .repositories.voice_budget import effective_settings, status
        current=effective_settings(database_path,settings) if enable_profiles else settings
        test_status=status(database_path,settings) if enable_profiles else None
        return {'provider': current.provider, 'model': current.model if current.provider == 'openai' else None,
                'testing_session':test_status,
                'configured': not settings.error and (settings.provider == 'mock' or bool(settings.api_key)),
                'voice_enabled': bool(enable_profiles and current.provider=='openai'),
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


app = create_app(settings=load(), enable_profiles=True)
