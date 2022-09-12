import os
import helper

ROOT_DIR = helper.backslash_to_forward_slash(os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir)))
VIDEO_FOLDER_PATH = f'{ROOT_DIR}/video'
VIDEO_CUTS_FOLDER_PATH = f'{ROOT_DIR}/video-cuts'
AUDIO_FOLDER_PATH = f'{ROOT_DIR}/audio'
TRANSCRIPTION_FOLDER_PATH = f'{ROOT_DIR}/transcription'
FINAL_FOLDER_PATH = f'{ROOT_DIR}/final'

WORD_SEARCH = set(["leroy"])
