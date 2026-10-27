import asyncio
import json
import base64
import sqlite3
from uuid import UUID
from fastapi import APIRouter, Response, WebSocket, WebSocketDisconnect
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from ..voice_schemas import VoiceSessionCreate, VoiceAction, VoiceStop, MockTurn, AudioTurn
from ..repositories import voice, conversations as chat
from ..controllers.voice import MockVoice
from ..identity import resolve, active_context, validate_context, IdentityError
from ..db import connect
from ..providers.voice import speak
from ..providers.live_voice import VoiceFailure
from ..crisis import review_response, NOTICE


def router(path, tasks, settings=None):
    api=APIRouter(prefix='/api/voice')
    provider=MockVoice(path,settings)
    mode="openai" if provider.live else "mock"

    @api.get('/conversations/{ident}/latest-turn')
    def latest_turn(ident:UUID):
        with chat.connection(path) as db:
            chat.owned(db,ident)
            row=db.execute('SELECT t.id FROM voice_turns t JOIN voice_sessions s ON s.id=t.session_id '
                           'WHERE s.conversation_id=? ORDER BY t.created_at DESC,t.sequence DESC LIMIT 1',(str(ident),)).fetchone()
            return {'turn':voice.turn_in(db,row[0]) if row else None}

    @api.post('/sessions')
    def create(body:VoiceSessionCreate,response:Response):
        result,fresh=voice.create(path,body)
        response.status_code=201 if fresh else 200
        return result | {'provider':mode,'persistence':'saved','replayed':not fresh}

    @api.get('/sessions/{ident}')
    def get(ident:UUID):
        result=voice.get(path,ident)
        for turn in result['turns']: turn['provider']=mode
        return result | {'provider':mode}

    @api.post('/sessions/{ident}/stop')
    def stop(ident:UUID,body:VoiceStop):
        result=voice.stop(path,ident,body)
        provider.clear(ident)
        return result | {'persistence':'saved'}

    @api.post('/turns/{ident}/actions')
    async def action(ident:UUID,body:VoiceAction):
        provider.prune()
        retained=provider.pending_replies.get(str(ident))
        with chat.connection(path) as db:
            current=voice.turn_in(db,ident)
        candidate = retained[2] if body.action=='retry_reply_save' and retained else (current['request'] or {}).get('assistant_content')
        if body.action != 'cancel' and candidate and review_response(candidate):
            return JSONResponse(status_code=422,content={'error':{'code':'response_unavailable','message':'This reply could not be provided within this app’s educational scope.','retryable':False},'persistence':'saved' if current['request'] and current['request']['assistant_persistence']=='saved' else 'not_saved'})
        result=voice.action(path,ident,body,retained[2] if retained else None)
        if body.action=='retry_reply_save':
            provider.pending_replies.pop(str(ident),None)
            return result
        if body.action=='cancel': provider.audio.pop(str(ident),None)
        else:
            try:
                if provider.live:
                    key=str(body.operation_id)+':speech-retry'
                    with chat.connection(path) as db:
                        receipt=db.execute('SELECT outcome FROM voice_provider_attempts WHERE operation_key=?',(key,)).fetchone()
                    if receipt:
                        # Never spend again for an exact replay, even after lost audio/restart.
                        return result
                    audio=await provider.speech_provider.speak(result['request']['assistant_content'],key)
                else: audio=await speak(result['request']['assistant_content'],'success')
            except (VoiceFailure,ValueError) as exc:
                return voice.update(path,ident,speech='failed',error_code=str(exc) if isinstance(exc,VoiceFailure) else 'speech_failed')
            # Revalidate after awaiting; switching/cancellation must invalidate late audio.
            with chat.connection(path) as db:
                current=voice.turn_in(db,ident)
                if current['state']=='cancelled': raise chat.Conflict('Turn was cancelled.')
            import time
            provider.prune()
            provider.audio[str(ident)]=(result['session_id'],time.monotonic()+300,audio)
            result=voice.update(path,ident,speech='ready',error_code=None)
        return result

    @api.get('/turns/{ident}/audio')
    def audio(ident:UUID):
        with chat.connection(path) as db:
            turn=voice.turn_in(db,ident)
            if turn['speech']!='ready' or not turn['request'] or turn['request']['assistant_persistence']!='saved':
                raise chat.Conflict('No saved reply audio is ready.')
        if review_response(turn['request']['assistant_content']):
            return JSONResponse(status_code=422,content={'error':{'code':'response_unavailable','message':'This saved reply is unavailable for playback.','retryable':False},'persistence':'saved'})
        provider.prune()
        cached=provider.audio.get(str(ident))
        if cached is None:
            return JSONResponse(status_code=410,content={'error':{'code':'audio_expired','message':'Audio expired. Text remains saved.','retryable':True},'persistence':'saved'})
        return Response(cached[2],media_type='audio/wav',headers={'Cache-Control':'no-store'})

    @api.websocket('/stream')
    async def stream(ws:WebSocket):
        origin=ws.headers.get('origin')
        if origin not in ('http://127.0.0.1:5173','http://localhost:5173'):
            await ws.close(code=1008); return
        await ws.accept()
        token=None; session_id=None; workers=set(); send_lock=asyncio.Lock()
        async def notify(event):
            async with send_lock:
                try: await ws.send_json(event)
                except (WebSocketDisconnect,RuntimeError): pass
        try:
            auth=await asyncio.wait_for(ws.receive_json(),5)
            if set(auth)!={'type','token','context_version','session_id'} or auth['type']!='authenticate':
                await ws.close(code=1008); return
            with connect(path) as db:
                identity=resolve(db,'Bearer '+str(auth['token']))
                if identity.version!=auth['context_version'] or not identity.owner_id:
                    raise IdentityError(409,'stale_context','Select your profile again.')
            token=active_context.set(identity)
            session_id=str(UUID(auth['session_id']))
            with chat.connection(path) as db:
                session=voice.session_in(db,session_id)
                if session['browser_session_id']!=identity.session_id or session['context_version']!=identity.version or session['state'] not in ('ready','active'):
                    raise chat.Conflict('Voice session is not active in this browser context.')
            await notify({'type':'ready','provider':mode,'microphone':'off'})
            while True:
                raw=await asyncio.wait_for(ws.receive_text(),60)
                if len(raw)>1281000: raise ValueError('Frame too large')
                event=json.loads(raw)
                if event.get('type')=='ping':
                    await notify({'type':'pong'}); continue
                audio_data=None
                if provider.live:
                    body=AudioTurn.model_validate(event)
                    from ..providers.live_voice import validate_wav
                    audio_data=validate_wav(base64.b64decode(body.audio,validate=True))
                else: body=MockTurn.model_validate(event)
                turn,fresh=voice.begin(path,session_id,body)
                await notify({'type':'accepted','turn_id':str(body.turn_id),'replayed':not fresh})
                if fresh:
                    task=asyncio.create_task(provider.process(session_id,body,notify,audio_data))
                    workers.add(task); tasks.add(task)
                    task.add_done_callback(workers.discard); task.add_done_callback(tasks.discard)
                else: await notify({'type':'status','session_id':session_id})
        except WebSocketDisconnect: pass
        except TimeoutError:
            await notify({'type':'stopped','message':'Mock session stopped after inactivity. Start again explicitly.'})
            try: await ws.close(code=1000)
            except RuntimeError: pass
        except (VoiceFailure, ValueError,ValidationError,IdentityError,chat.NotFound,chat.Conflict,sqlite3.Error) as exc:
            code=exc.code if isinstance(exc,IdentityError) else 'voice_connection_failed'
            await notify({'type':'error','code':code,'message':'Voice connection stopped. Read status before retrying.'})
            try: await ws.close(code=1008)
            except RuntimeError: pass
        finally:
            # Close never resumes capture or resubmits a turn. Cancel only pending work.
            for task in workers: task.cancel()
            if workers: await asyncio.gather(*workers,return_exceptions=True)
            if session_id and token is not None:
                try:
                    from ..voice_schemas import VoiceStop
                    from uuid import uuid4
                    current=voice.get(path,session_id)
                    if current['state'] in ('ready','active'):
                        voice.stop(path,session_id,VoiceStop(operation_id=uuid4(),expected_revision=current['revision']))
                except (sqlite3.Error,IdentityError,chat.NotFound,chat.Conflict): pass
                provider.clear(session_id)
            if token is not None: active_context.reset(token)
    return api
