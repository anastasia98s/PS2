import contextlib
import sys
import torch

DEVICE = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

TTS_TRAINED_PATH = 'data/model_file.pth'
TTS_JSON_PATH = 'data/config.json'

def_reference_wav = None
def_reference_speaker_idx = None
def_capacitron_style_text = None
def_capacitron_style_wav = None
def_speaker_wav = None
def_language_idx = None
def_speaker_idx = None

def_voice_dir = None
def_language_ids_file_path = None
def_speakers_file_path = None
def_pipe_out = False

pipe_out = sys.stdout if def_pipe_out else None

with contextlib.redirect_stdout(None if def_pipe_out else sys.stdout):
    tts_path = None
    tts_config_path = None
    speakers_file_path = None
    language_ids_file_path = None
    vocoder_path = None
    vocoder_config_path = None
    encoder_path = None
    encoder_config_path = None
    vc_path = None
    vc_config_path = None
    model_dir = None

    if TTS_TRAINED_PATH is not None:
        tts_path = TTS_TRAINED_PATH
        tts_config_path = TTS_JSON_PATH
        speakers_file_path = def_speakers_file_path
        language_ids_file_path = def_language_ids_file_path