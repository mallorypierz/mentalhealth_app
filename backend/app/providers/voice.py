"""Offline fixtures only. No microphone recognition or model speech is claimed."""
import asyncio
import io
import math
import struct
import wave

MOCK_TRANSCRIPT = 'What happened in my last breathing practice?'

async def transcribe(scenario):
    await asyncio.sleep(2 if scenario == 'delayed' else .35)
    if scenario == 'transcription_failure':
        raise ValueError('transcription_failed')
    return MOCK_TRANSCRIPT

async def speak(saved_text, scenario):
    await asyncio.sleep(.15)
    if scenario == 'speech_failure':
        raise ValueError('speech_failed')
    if not saved_text.strip():
        raise ValueError('empty_reply')
    # An intentionally non-speech fixture: never describe this tone as a spoken reply.
    output=io.BytesIO()
    with wave.open(output,'wb') as audio:
        audio.setnchannels(1); audio.setsampwidth(2); audio.setframerate(24000)
        samples=[int(2000*math.sin(2*math.pi*440*i/24000)*min(1,i/240,(7200-i)/240)) for i in range(7200)]
        audio.writeframes(struct.pack('<'+'h'*len(samples),*samples))
    return output.getvalue()
