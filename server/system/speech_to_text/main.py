import api
import config
from fastapi import FastAPI
from typing import List
import uvicorn
import whisper
import numpy as np

app = FastAPI()
recognizer = whisper.load_model(config.SPEECH_RECOGNITION_MODELL, config.DEVICE)

@app.post("/speech_to_text/recognize")
def recognize(signal: List[float]):
    try:
        signal = np.array(signal, dtype=np.float32)
        #signal = signal.astype(np.float32)
        signal = whisper.pad_or_trim(signal)
        result = recognizer.transcribe(signal, language=config.WHISPER_SPRACHE)
        sr_text = result["text"]
        if sr_text:
            no_speech_prob = result['segments'][0]['no_speech_prob']
            if no_speech_prob < config.NO_SPEECH_MAX_NOTEN:
                return {"result": sr_text.strip()}
            else:
                return {"result": None}
        else:
            return {"result": None}
    except Exception as e:
        return {"result": None}

if __name__ == "__main__":
    uvicorn.run("main:app", host=api.SPEECH_TO_TEXT_SERVICE_IP, port=api.SPEECH_TO_TEXT_SERVICE_PORT)