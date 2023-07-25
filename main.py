import os
from dotenv import load_dotenv
import openai

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

# Get path to video file with Python
video_file_path = os.path.join(os.getcwd(), "sample.mp4")

try:
    try:
        with open(video_file_path, "rb") as audio_file:
            translation = openai.Audio.translate(
                model="whisper-1",
                file=audio_file,
                response_format="srt"
            )
            # Output translation to text with timestamps
            with open("translation.txt", "w") as text_file:
                text_file.write(str(translation))
    except Exception as e:
        print("Error: ", e)
    try:
        with open(video_file_path, "rb") as audio_file:
            transcription = openai.Audio.transcribe(
                model="whisper-1",
                file=audio_file,
                response_format="srt"
            )
            # Output transcription to text with timestamps
            with open("transcription.txt", "w") as text_file:
                text_file.write(str(transcription))
    except Exception as e:
        print("Error: ", e)
except Exception as e:
    print("Error: ", e)
