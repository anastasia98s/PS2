import config
import api
from fastapi import FastAPI, Body
from typing import Dict, Any, List
from nn_authentifizierung.predictor import Predictor
import uvicorn
import numpy as np
from user_controller.model_user import ModelUser
from nn_authentifizierung.utils import extract_features
from nn_authentifizierung  import train
import os

app = FastAPI()
benutzerdatenbank = ModelUser()

def ensure_jsonable(obj):
    if isinstance(obj, np.ndarray):
        return obj.tolist()
    elif isinstance(obj, list):
        return [ensure_jsonable(item) for item in obj]
    elif isinstance(obj, (np.float32, np.float64)):
        return float(obj)
    elif isinstance(obj, (np.int32, np.int64)):
        return int(obj)
    else:
        return obj

@app.post("/kontoverwaltung/authentifizierung")
def authentifizierung(signal: List[float]):
    if os.path.exists(config.AUTHENTIFIZIERUNG_TRAINED_PATH):
        predictor_user = Predictor(config.AUTHENTIFIZIERUNG_TRAINED_PATH)

        signal = np.array(signal, dtype=np.float32)
        name_index, name_label = predictor_user.predict(signal)
        pred_id = int(name_label[0][name_index[0]])
        pred_noten = name_label[1][name_index[0]]

        print(f"Authentifizierungsnote: {str(pred_noten)}")

        if pred_noten < config.AUTHENTIFIZIERUNG_MIN_NOTEN:
            pred_id = None
        else:
            pred_id = int(name_label[0][name_index[0]])

        name_label = ensure_jsonable(name_label)
    else:
        pred_id = None
        name_label = []

    return {"pred_id": pred_id, "name_label": name_label}

@app.post("/kontoverwaltung/show_benutzer_name")
def show_benutzer_name(id: int = Body(...)):
    return {"result": benutzerdatenbank.show_benutzer_name(id)}

@app.post("/kontoverwaltung/add_benutzer")
def add_benutzer(name: str = Body(...)):
    return {"result": benutzerdatenbank.add_benutzer(name)}

@app.post("/kontoverwaltung/save_features")
def save_features(item: Dict[Any, Any]):
    signal = item.get("signal")
    benutzer_id = item.get("benutzer_id")

    signal = np.array(signal, dtype=np.float32)
    target_length = config.AUDIO_SIGNAL_LENGTH_SAVE
    signal_length = len(signal)
    num_parts = (signal_length - target_length) // target_length
    
    for i in range(num_parts):
        signal_part = signal[i * target_length : (i + 1) * target_length]
        features = extract_features(signal_part, api.AUDIO_SAMPLE_RATE)
        benutzerdatenbank.add_merkmale(benutzer_id, features)
    
    remainder_length = signal_length % target_length
    if remainder_length > 0:
        signal_part = signal[num_parts * target_length:]
        features = extract_features(signal_part, api.AUDIO_SAMPLE_RATE)
        benutzerdatenbank.add_merkmale(benutzer_id, features)
    
    train.train()

    return True

""" @app.post("/kontoverwaltung/train_authentifizierung_ki")
def train_authentifizierung_ki():
    train.train()
    return True """


@app.post("/kontoverwaltung/add_todo")
def add_todo(item: Dict[Any, Any]):
    aktivitaet = item.get("aktivitaet")
    datezeit = item.get("datezeit")
    benutzer_id = item.get("benutzer_id")
    return {"result": benutzerdatenbank.add_todo(aktivitaet, datezeit, benutzer_id)}

@app.post("/kontoverwaltung/show_todo")
def show_todo(item: Dict[Any, Any]):
    aktivitaet = item.get("aktivitaet")
    datum = item.get("datum")
    datezeit = item.get("datezeit")
    benutzer_id = item.get("benutzer_id")
    return {"result": benutzerdatenbank.show_todo(aktivitaet, datum, datezeit, benutzer_id)}

@app.post("/kontoverwaltung/delete_todo")
def delete_todo(item: Dict[Any, Any]):
    aktivitaet = item.get("aktivitaet")
    datum = item.get("datum")
    datezeit = item.get("datezeit")
    benutzer_id = item.get("benutzer_id")
    return {"result": benutzerdatenbank.delete_todo(aktivitaet, datum, datezeit, benutzer_id)}

if __name__ == "__main__":
    uvicorn.run("main:app", host=api.KONTOVERWALTUNG_SERVICE_IP, port=api.KONTOVERWALTUNG_SERVICE_PORT)