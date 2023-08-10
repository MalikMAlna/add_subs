import os
from dotenv import load_dotenv
import openai
from moviepy.editor import TextClip, VideoFileClip, CompositeVideoClip
from moviepy.video.tools.subtitles import SubtitlesClip
import argparse

parser = argparse.ArgumentParser(description="Add subtitles to video")
parser.add_argument("-v", "--video", help="Path to video file", default="sample.mp4")
args = parser.parse_args()
config = vars(args)

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

# Get path to video file with Python
video_file_path = config.get("video")

try:
    try:
        with open(video_file_path, "rb") as audio_file:
            translation = openai.Audio.translate(
                model="whisper-1",
                file=audio_file,
                response_format="srt"
            )
            # Output translation to text with timestamps
            with open("translation.srt", "w") as output_file:
                last_line_num = int(
                    translation.rstrip('\n').split('\n')[-3]
                ) + 1
                last_timestamp = translation.rstrip('\n').split('\n')[-2]

                """
                `.rstrip('\n')` removes the last newlines of the output
                that mess with the formatting of the srt file
                Also had to add an extra line at the end of the file
                with the last line number and timestamp
                to make sure the srt file is formatted correctly
                And picks up the actual last line of the translation
                """

                output_file.write(
                    str(translation).rstrip('\n') +
                    f"\n\n{last_line_num}\n{last_timestamp}"
                )
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
            with open("transcription.srt", "w") as output_file:
                last_line_num = int(
                    transcription.rstrip('\n').split('\n')[-3]
                ) + 1
                last_timestamp = transcription.rstrip('\n').split('\n')[-2]
                output_file.write(
                    str(transcription).rstrip('\n') +
                    f"\n\n{last_line_num}\n{last_timestamp}"
                )
    except Exception as e:
        print("Error: ", e)
except Exception as e:
    print("Error: ", e)

# Add subtitles to original video
# Feel free to change to trascription or translation
# Also, feel free to change the font, fontsize, and color
srt_file_path = os.path.join(os.getcwd(), "translation.srt")


def generate_text(txt):
    return TextClip(txt, font='Arial', fontsize=32, color='white')


subs = SubtitlesClip(srt_file_path, generate_text)
subtitles = SubtitlesClip(subs, generate_text)
video = VideoFileClip(video_file_path)
result = CompositeVideoClip(
    [video, subtitles.set_pos(('center', 'bottom'))]
)
result.write_videofile("output.mp4",
                       fps=video.fps,
                       temp_audiofile="temp-audio.m4a",
                       remove_temp=True,
                       codec="libx264",
                       audio_codec="aac"
                       )
