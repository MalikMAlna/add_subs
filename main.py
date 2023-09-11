import os
from dotenv import load_dotenv
import openai
from moviepy.editor import TextClip, VideoFileClip, CompositeVideoClip
from moviepy.video.tools.subtitles import SubtitlesClip
import argparse

parser = argparse.ArgumentParser(description="Add subtitles to video")
parser.add_argument("-v", "--video", help="Path to video file", default="sample.mp4")
parser.add_argument("-t", "--type", help="Process type: translate or transcribe", default="translate")
args = parser.parse_args()
config = vars(args)

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

def process_audio(file_path, process_type):                                   
    try:                                                                      
        with open(file_path, "rb") as audio_file:                             
            if process_type == 'translate':                                   
                result = openai.Audio.translate(                              
                    model="whisper-1",                                        
                    file=audio_file,                                          
                    response_format="srt"                                     
                )                                                             
            elif process_type == 'transcribe':                                
                result = openai.Audio.transcribe(                             
                    model="whisper-1",                                        
                    file=audio_file,                                          
                    response_format="srt"                                     
                )                                                             
            else:                                                             
                raise ValueError('Invalid process type. Choose either translate or transcribe.')                                                    
            return result                                                     
    except Exception as e:                                                    
        print("Error: ", e)

def write_to_file(result, output_file):                                       
    try:                                                                      
        with open(output_file, "w") as file:
            """
            `.rstrip('\n')` removes the last newlines of the output
            that mess with the formatting of the srt file
            Also had to add an extra line at the end of the file
            with the last line number and timestamp
            to make sure the srt file is formatted correctly
            And picks up the actual last line of the translation
            """                                  
            last_line_num = int(result.rstrip('\n').split('\n')[-3]) + 1      
            last_timestamp = result.rstrip('\n').split('\n')[-2]              
            file.write(str(result).rstrip('\n') +                             
f"\n\n{last_line_num}\n{last_timestamp}")                                     
    except Exception as e:                                                    
        print("Error: ", e)
        

def add_subtitles(video_file_path, srt_file_path):                            
    try:                                                                      
        def generate_text(txt):                                               
            return TextClip(txt, font="Arial", fontsize=32, color='white')    
        subs = SubtitlesClip(srt_file_path, generate_text, encoding='utf-8')                    
        video = VideoFileClip(video_file_path)                                
        result = CompositeVideoClip([video, subs.set_position(('center',           
'bottom'))])                                                                  
        result.write_videofile("output.mp4",                                  
                               fps=video.fps,                                 
                               temp_audiofile="temp-audio.m4a",               
                               remove_temp=True,                              
                               codec="libx264",                               
                               audio_codec="aac")                             
    except Exception as e:                                                    
        print("Error: ", e)

def main():                                                                   
    # Get path to video file with Python
    video_file_path = config.get("video")

    output_file = os.path.join(os.getcwd(), "output.srt")                                              

    # Process the audio from the video file                                   
    result = process_audio(video_file_path, config.get("type"))                      

    # Write the result to a file                                              
    write_to_file(result, output_file)                                        

    # Add subtitles to the video                                              
    add_subtitles(video_file_path, output_file)                               

if __name__ == "__main__":                        
    main()   