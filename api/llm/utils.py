from openai import OpenAI
from decouple import config
from pathlib import Path

client = OpenAI(api_key=config('OPENAI_API_KEY'))

DIR_PATH = Path(__file__).resolve().parent.parent


def tts_file(text, file_name='speech.mp3'):
    """
    Text to speech function.
    Accepts the text to be converted to speech.
    Returns the audio file in bytes.
    """
    res = client.audio.speech.create(
        model="tts-1",
        voice="alloy",
        input=text,
    )
    res.stream_to_file(DIR_PATH / 'media' / 'voices' / file_name)


def tts(text):
    """
    Text to speech function.
    Accepts the text to be converted to speech.
    Returns the audio file in bytes.
    """
    res = client.audio.speech.create(
        model="tts-1",
        voice="alloy",
        input=text,
        response_format="aac"
    )
    return res


def stt(content: bytes):
    """
    Speech to text function.
    Accepts the audio file in bytes.
    Returns the transcript.
    """
    transcript = client.audio.transcriptions.create(
        model="whisper-1",
        file=content,
        language='en',
        response_format='text'
    )
    return transcript
