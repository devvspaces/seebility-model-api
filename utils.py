import openai
from pathlib import Path
from pydub.playback import play
from pydub import AudioSegment
from dotenv import load_dotenv
from openai import OpenAI
import os
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI()


#text to speech function

#accepts text from  the assistant to be voiced out

def tts(text):
    speech_file_path = Path().parent / "speech.mp3"
    res= client.audio.speech.create(
    model="tts-1",
    voice="alloy",
    input=text
    )
    res.stream_to_file(speech_file_path)
    sound=AudioSegment.from_mp3(speech_file_path)
    play(sound)



#speech to text function
        #accepts the path to the audio to be transcibed
def stt(path):
    audio_file= open(path, "rb")
    transcript = client.audio.transcriptions.create(
    model="whisper-1", 
    file=audio_file,
    language='en',
    response_format='text'
    )
    return transcript