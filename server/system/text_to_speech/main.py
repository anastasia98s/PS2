import api
import config
import os
import numpy as np
import torch
import base64
from TTS.utils.synthesizer import Synthesizer    
from fastapi import FastAPI, Body
import uvicorn
from io import BytesIO
import scipy
import re

if not os.path.isfile(config.TTS_TRAINED_PATH) or not os.path.isfile(config.TTS_JSON_PATH):
    raise FileNotFoundError(f"\nTTS Modell / TTS Config nicht gefunden")

synthesizer = Synthesizer(
    config.tts_path,
    config.tts_config_path,
    config.speakers_file_path,
    config.language_ids_file_path,
    config.vocoder_path,
    config.vocoder_config_path,
    config.encoder_path,
    config.encoder_config_path,
    config.vc_path,
    config.vc_config_path,
    config.model_dir,
    config.def_voice_dir).to(api.DEVICE)

app = FastAPI()

@app.post("/text_to_speech/generieren")
def generieren(text: str = Body(...)):
    if text:
        text = re.sub(r'\.|\:00', '', text) # Da unser aktuelles TTS Datum und Uhrzeit nicht richtig lesen kann.
        wav = synthesizer.tts(
            text,
            speaker_name=config.def_speaker_idx,
            language_name=config.def_language_idx,
            speaker_wav=config.def_speaker_wav,
            reference_wav=config.def_reference_wav,
            style_wav=config.def_capacitron_style_wav,
            style_text=config.def_capacitron_style_text,
            reference_speaker_name=config.def_reference_speaker_idx,
        )
        if torch.is_tensor(wav):
            wav = wav.cpu().numpy()
        if isinstance(wav, list):
            wav = np.array(wav)

        wav_norm = wav * (32767 / max(0.01, np.max(np.abs(wav))))
        wav_norm = wav_norm.astype(np.int16)
        
        byte_io = BytesIO()
        scipy.io.wavfile.write(byte_io, 22050, wav_norm)
        wav_bytes = byte_io.getvalue()

        wav_encode = base64.b64encode(wav_bytes).decode('utf-8')
        return {"result": wav_encode}
    else:
        return {"result": None}

if __name__ == "__main__":
    uvicorn.run("main:app", host=api.TEXT_TO_SPEECH_SERVICE_IP, port=api.TEXT_TO_SPEECH_SERVICE_PORT)