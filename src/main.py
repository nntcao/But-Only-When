import glob
import pickle
import json
import datetime

import video
import helper
import transcription

from settings import *

def main():
    print("audio")
    generate_audio_from_video()

    print("transcription")
    generate_transcription_from_audio()
    
    print("video interval")
    vid_intervals_list = generate_intervals_from_transcription()
    generate_video_cuts_from_intervals(vid_intervals_list)

    write_video_cut_paths()
    
    video_final_path = f"{FINAL_FOLDER_PATH}/final.mp4"
    video.stitch_videos(video_final_path)

def cleanup():
    audio_paths_list = glob.glob(f'{AUDIO_FOLDER_PATH}/*')
    transcriptions_paths_list = glob.glob(f'{TRANSCRIPTION_FOLDER_PATH}/*')
    video_cut_paths_list = glob.glob(f'{VIDEO_CUTS_FOLDER_PATH}/*')
    files = audio_paths_list + transcriptions_paths_list + video_cut_paths_list
    for f in files:
        os.remove(f)

def generate_audio_from_video(): 
    video_paths_list = glob.glob(f'{VIDEO_FOLDER_PATH}/*')
    for video_path in video_paths_list:
        filename = helper.strip_filename_from_path(video_path)
        audio_path = f'{AUDIO_FOLDER_PATH}/{filename}.wav'
        video.convert_to_audio(video_path, audio_path)

def generate_transcription_from_audio():
    audio_paths_list = glob.glob(f'{AUDIO_FOLDER_PATH}/*')
    for audio_path in audio_paths_list:
        filename = helper.strip_filename_from_path(audio_path)
        transcription.wav_to_textresult(audio_path)

def generate_intervals_from_transcription():
    transcriptions_paths_list = glob.glob(f'{TRANSCRIPTION_FOLDER_PATH}/*')
    intervals = [[] * len(transcriptions_paths_list)]
    for i, transcription_path in enumerate(transcriptions_paths_list):
        with open(transcription_path, 'rb') as handle:
            transcription = pickle.load(handle)
            for transcription_string in transcription:
                transcription_dict = json.loads(transcription_string)
                for word_dict in transcription_dict["result"]:
                    if word_dict["word"] in WORD_SEARCH:
                        start_time = str(datetime.timedelta(seconds=word_dict["start"]))
                        end_time = str(datetime.timedelta(seconds=word_dict["end"]))
                        intervals[i].append((start_time, end_time))
    return intervals
    
def generate_video_cuts_from_intervals(vid_intervals_list):
    video_paths_list = glob.glob(f'{VIDEO_FOLDER_PATH}/*')
    counter = 1
    for i, intervals_list in enumerate(vid_intervals_list):
        video_path = video_paths_list[i]
        for start_time, end_time in intervals_list:
            output_path = f'{VIDEO_CUTS_FOLDER_PATH}/{counter}.mp4'
            video.cut_video(
                file=video_path, 
                output=output_path, 
                start=start_time, 
                end=end_time)
            counter += 1

def write_video_cut_paths():
    video_cut_paths_list = glob.glob(f'{VIDEO_CUTS_FOLDER_PATH}/*')
    video_cut_paths_list = sorted(video_cut_paths_list)

    video_cut_txt_path = f"{VIDEO_CUTS_FOLDER_PATH}/video_cuts.txt"
    if os.path.exists(video_cut_txt_path):
        os.remove(video_cut_txt_path)

    f = open(video_cut_txt_path, "a")
    for video_cut_path in video_cut_paths_list:
        f.write(f"file {helper.backslash_to_forward_slash(video_cut_path)}\n")
    f.close()

cleanup()
main()