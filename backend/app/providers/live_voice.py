"""Bounded OpenAI audio calls. No disk audio, SDK retries or response-body logs."""
import asyncio
import io
import wave
import json
import httpx
from ..repositories import voice_budget
from ..repositories.provider_usage import LimitError

class VoiceFailure(Exception): pass

def validate_wav(data):
    if not 44 <= len(data) <= 960044: raise VoiceFailure('invalid_audio')
    try:
        with wave.open(io.BytesIO(data),'rb') as wav:
            if wav.getnchannels()!=1 or wav.getsampwidth()!=2 or wav.getframerate()!=16000 or wav.getcomptype()!='NONE':
                raise VoiceFailure('invalid_audio')
            frames=wav.getnframes()
            if not 3200 <= frames <= 480000 or len(wav.readframes(frames))!=frames*2: raise VoiceFailure('invalid_audio')
    except (wave.Error,EOFError): raise VoiceFailure('invalid_audio') from None
    return data

class AudioProvider:
    def __init__(self,path,settings,transport=None):
        self.path,self.settings,self.transport=path,settings,transport

    async def call(self,key,stage,route,**kwargs):
        try: ident=voice_budget.reserve(self.path,key,stage,self.settings)
        except (ValueError,LimitError) as exc: raise VoiceFailure(str(exc)) from None
        try:
            async with asyncio.timeout(30):
                async with httpx.AsyncClient(transport=self.transport,trust_env=False,follow_redirects=False,
                    timeout=httpx.Timeout(30,connect=5)) as client:
                    async with client.stream('POST','https://api.openai.com/v1/audio/'+route,
                        headers={'Authorization':'Bearer '+self.settings.api_key},**kwargs) as response:
                        response.raise_for_status()
                        raw=bytearray()
                        async for chunk in response.aiter_bytes():
                            raw.extend(chunk)
                            if len(raw)>(4000000 if stage=='speech' else 32768): raise VoiceFailure('audio_response_too_large')
            voice_budget.finish(self.path,ident,'succeeded')
            return bytes(raw)
        except asyncio.CancelledError:
            voice_budget.finish(self.path,ident,'interrupted'); raise
        except (TimeoutError,httpx.TimeoutException): code='provider_timeout'
        except httpx.HTTPStatusError as exc: code=f'provider_http_{exc.response.status_code}'
        except httpx.HTTPError: code='provider_connection_failure'
        except VoiceFailure as exc: code=str(exc)
        voice_budget.finish(self.path,ident,code)
        raise VoiceFailure(code)

    async def transcribe(self,audio,key):
        validate_wav(audio)
        raw=await self.call(key,'transcription','transcriptions',
            data={'model':'gpt-4o-mini-transcribe','response_format':'json'},files={'file':('utterance.wav',audio,'audio/wav')})
        try:
            text=json.loads(raw)['text']
            if not isinstance(text,str) or not text.strip() or len(text)>2000: raise ValueError()
            return text.strip()
        except (ValueError,KeyError,TypeError): raise VoiceFailure('invalid_transcription') from None

    async def speak(self,text,key):
        if not text or len(text)>600: raise VoiceFailure('speech_text_too_long')
        raw=await self.call(key,'speech','speech',json={'model':'gpt-4o-mini-tts','voice':'marin','input':text,'response_format':'pcm'})
        return pcm_to_wav(raw)


def pcm_to_wav(raw):
    # Speech API PCM: mono 24kHz signed 16-bit little endian. Build an exact
    # file header from received samples, not a streaming WAV length sentinel.
    if not raw or len(raw)%2 or len(raw)>4000000:
        raise VoiceFailure('invalid_speech')
    output=io.BytesIO()
    with wave.open(output,'wb') as wav:
        wav.setnchannels(1); wav.setsampwidth(2); wav.setframerate(24000)
        wav.writeframes(raw)
    return output.getvalue()
