import asyncio
import sqlite3
import time
from ..repositories import voice, conversations as chat
from ..chat_schemas import MessageSubmit
from ..providers import voice as fixtures, mock
from ..rag.pipeline import run, RAGFailure
from ..identity import owner
from ..providers.live_voice import AudioProvider, VoiceFailure
from ..providers.openai import Provider
from ..repositories.voice_budget import RAGLedger
from ..crisis import matches, NOTICE, review_response

class MockVoice:
    """Per-app bounded ephemeral audio; live calls require explicit configuration."""
    def __init__(self, path, settings=None):
        self.path=path
        self.settings=settings
        self.live=bool(settings and settings.voice_enabled and settings.voice_prices_verified and settings.api_key and not settings.error)
        self.speech_provider=AudioProvider(path,settings) if self.live else None
        self.audio={}
        self.pending_replies={}

    def clear(self, session_id):
        self.pending_replies={key:value for key,value in self.pending_replies.items() if value[0]!=str(session_id)}
        self.audio={key:value for key,value in self.audio.items() if value[0]!=str(session_id)}

    def prune(self):
        self.pending_replies={key:value for key,value in self.pending_replies.items() if value[1]>time.monotonic()}
        self.audio={key:value for key,value in self.audio.items() if value[1]>time.monotonic()}

    async def process(self, session_id, body, notify, audio_data=None):
        ident=str(body.turn_id)
        try:
            text=await self.speech_provider.transcribe(audio_data,ident+':transcription') if self.live else await fixtures.transcribe(body.scenario)
            current=voice.update(self.path,ident,transcription='succeeded')
            if current['state']=='cancelled': return
            if matches(text):
                if voice.hold_for_support(self.path,ident):
                    self.clear(session_id)
                    await notify({'type':'support_notice','turn_id':ident,'text':text,'message':NOTICE,
                                  'submission':'not_saved','transcription_provider':'openai' if self.live else 'mock'})
                return
            await notify({'type':'transcript','turn_id':ident,'text':text,'mock':not self.live})
            # No await between ownership/cancellation check and atomic ordinary submission.
            with chat.connection(self.path) as db:
                if voice.turn_in(db,ident)['state']=='cancelled': return
                conversation=voice.session_in(db,session_id)['conversation_id']
            try:
                status,_=chat.submit(self.path,conversation,MessageSubmit(request_id=body.request_id,content=text),provider='openai' if self.live else 'mock', model=self.settings.model if self.live else None)
                voice.update(self.path,ident,request_id=status['id'],submission='saved')
            except sqlite3.Error:
                voice.update(self.path,ident,state='failed',submission='unknown',error_code='transcript_save_failed')
                return
            await notify({'type':'submitted','turn_id':ident,'request_id':status['id']})
            claimed=chat.claim(self.path,body.request_id)
            if not claimed: return
            _,content,conversation,before_sequence=claimed
            try:
                reply,outcome,citations,ids=await run(self.path,content,owner(),conversation,before_sequence,
                    'failure' if getattr(body,'scenario','success')=='model_failure' else 'success',
                    Provider(self.path,body.request_id,self.settings,ledger=RAGLedger()) if self.live else mock,
                    lambda stage: chat.count_call(self.path,body.request_id,stage))
                chat.retrieval_status(self.path,body.request_id,outcome,ids,citations)
            except RAGFailure as exc:
                chat.retrieval_status(self.path,body.request_id,exc.code,stage=exc.stage)
                chat.fail(self.path,body.request_id,exc.code)
                voice.update(self.path,ident,state='failed',error_code=exc.code)
                return
            try:
                chat.finish(self.path,body.request_id,reply)
            except sqlite3.Error:
                self.prune()
                if len(self.pending_replies)>=8: self.pending_replies.pop(next(iter(self.pending_replies)))
                self.pending_replies[ident]=(str(session_id),time.monotonic()+300,reply)
                chat.fail(self.path,body.request_id,'reply_save_failed')
                voice.update(self.path,ident,state='failed',error_code='reply_save_failed')
                return
            saved=chat.get_status(self.path,body.request_id)
            if saved['assistant_persistence']!='saved': return
            # Recheck before audio, including replies that could have been saved earlier.
            review_code=review_response(saved['assistant_content'])
            if review_code:
                voice.update(self.path,ident,state='completed',speech='blocked',error_code=review_code)
                return
            voice.update(self.path,ident,speech='processing')
            try:
                audio=await self.speech_provider.speak(saved['assistant_content'],ident+':speech') if self.live else await fixtures.speak(saved['assistant_content'],body.scenario)
            except (ValueError,VoiceFailure) as exc:
                voice.update(self.path,ident,state='completed',speech='failed',error_code=str(exc) if isinstance(exc,VoiceFailure) else 'speech_failed')
                return
            with chat.connection(self.path) as db:
                current=voice.turn_in(db,ident)
                session=voice.session_in(db,session_id)
            if current['state']=='cancelled' or session['state'] not in ('ready','active'): return
            self.prune()
            if len(self.audio)>=8:
                self.audio.pop(next(iter(self.audio)))
            self.audio[ident]=(str(session_id),time.monotonic()+300,audio)
            voice.update(self.path,ident,state='completed',speech='ready')
        except (ValueError,VoiceFailure) as exc:
            voice.update(self.path,ident,state='failed',transcription='failed',error_code=str(exc) if isinstance(exc,VoiceFailure) else 'transcription_failed')
        except asyncio.CancelledError:
            raise
        except (sqlite3.Error, chat.Conflict):
            # Read persisted state to reconcile; never report an unconfirmed save as success.
            return
        finally:
            await notify({'type':'status','session_id':str(session_id)})
