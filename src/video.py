import os
import subprocess
from settings import *

def convert_to_audio(file: str, output: str):
    command = f"ffmpeg \
        -hide_banner \
        -loglevel error \
        -i {file} \
        -ar 16000 \
        -ac 1 \
        -acodec pcm_s16le \
        {output}"
    subprocess.call(command)

def cut_video(file: str, output: str, start: str, end: str):
    command = f"ffmpeg \
        -hide_banner \
        -loglevel error \
        -ss {start} \
        -to {end} \
        -i {file} \
        -c:v copy \
        -c:a copy \
        {output}"
    subprocess.call(command)

def stitch_videos(output: str):
    video_cut_txt_path = f"{VIDEO_CUTS_FOLDER_PATH}/video_cuts.txt"
    
    command = f"ffmpeg \
        -hide_banner \
        -loglevel error \
        -f concat \
        -safe 0 \
        -i {video_cut_txt_path} \
        {output}"
    subprocess.call(command)
