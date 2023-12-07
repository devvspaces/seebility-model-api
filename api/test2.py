import base64
from pydub import AudioSegment
from llm.utils import tts_file


def convert_mp3_to_opus(mp3_file, opus_file):
    # Load the MP3 file
    audio = AudioSegment.from_mp3(mp3_file)

    # Export as Opus format with the desired bitrate (e.g., 128 kbps)
    audio.export(opus_file, format="opus", bitrate="128k")


def audio_to_base64(file_path):
    try:
        with open(file_path, "rb") as audio_file:
            # Read the audio file as binary data
            audio_binary = audio_file.read()

            # Encode the binary audio data as Base64
            base64_encoded = base64.b64encode(audio_binary).decode('utf-8')
            return base64_encoded

    except FileNotFoundError:
        print("File not found.")
        return None
    except Exception as e:
        print("Error:", e)
        return None


# audio_path = "llm/speech.mp3"
# audio_path = "llm/speech1.wav"
# audio_path = "llm/speech.opus"

# base64_audio = audio_to_base64(audio_path)


# with open("base64.txt", "w") as f:
#     f.write(base64_audio)

# Example usage
# mp3_input_file = "llm/speech.mp3"  # Replace with your input MP3 file path
# # Replace with the desired output Opus file path
# opus_output_file = "llm/speech.opus"

# convert_mp3_to_opus(mp3_input_file, opus_output_file)


voices = [
    {
        "text": "Hey, tap your screen! Tell Us What You Want.",
        "file_name": "welcome.mp3"
    },
    {
        "text": "I am currently surfing the web for you for products that match your request.",
        "file_name": "wait.mp3"
    },
]


for voice in voices:
    tts_file(voice["text"], voice["file_name"])
