#!/usr/bin/env python3
import wave
import pickle
import helper
from settings import *
from vosk import Model, KaldiRecognizer, SetLogLevel


SetLogLevel(-1)
model_path = r"C:\projects\but-only-when\models\vosk-model-en-us-0.22"

def wav_to_textresult(file):
    wf = wave.open(file, "rb")

    if wf.getnchannels() != 1:
        print ("Audio file must be WAV format mono.")
        exit (1)
    if wf.getsampwidth() != 2:
        print("Audio file must be WAV format PCM.")
        exit (1)
    if wf.getcomptype() != "NONE":
        print("Audio file must be WAV format.")
        exit (1)

    model = Model(model_path)

    rec = KaldiRecognizer(model, wf.getframerate())
    rec.SetWords(True)
    rec.SetPartialWords(True)

    results = []
    while True:
        data = wf.readframes(4000)
        if len(data) == 0:
            break
        if rec.AcceptWaveform(data):
            results.append(rec.Result())
    rec.FinalResult()
    
    filename = helper.strip_filename_from_path(file)
    with open(f'{TRANSCRIPTION_FOLDER_PATH}/{filename}.pickle', 'wb') as handle:
        pickle.dump(results, handle, protocol=pickle.HIGHEST_PROTOCOL)