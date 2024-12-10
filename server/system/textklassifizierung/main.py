import api
import config
from fastapi import FastAPI, Body
from typing import Dict, Any
from nn_textklassifizierung.predictor import Predictor
import uvicorn
import numpy as np
from textklassifizierung_controller.model_textklassifizierung import ModelTextklassifizierung

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

predictor_text = Predictor(config.TEXTKLASSIFIZIERUNG_TRAINED_PATH)

app = FastAPI()
@app.post("/textklassifizierung/klassifizieren")
def klassifizieren(text: str = Body(...)):
    anmerkung_satz_labels, woerter_anmerkungen, absicht_satz_labels, absicht_class_scores, szenario_satz_labels, szenario_class_scores = predictor_text.predict(text)
    
    anmerkung_satz_labels = ensure_jsonable(anmerkung_satz_labels)
    woerter_anmerkungen = ensure_jsonable(woerter_anmerkungen)
    absicht_satz_labels = ensure_jsonable(absicht_satz_labels)
    szenario_satz_labels = ensure_jsonable(szenario_satz_labels)
    absicht_class_scores = ensure_jsonable(absicht_class_scores)
    szenario_class_scores = ensure_jsonable(szenario_class_scores)
    
    return {
        "anmerkung_satz_labels": anmerkung_satz_labels,
        "woerter_anmerkungen": woerter_anmerkungen,
        "absicht_satz_labels": absicht_satz_labels,
        "absicht_class_scores": absicht_class_scores,
        "szenario_satz_labels": szenario_satz_labels,
        "szenario_class_scores": szenario_class_scores
    }

@app.post("/textklassifizierung/add_verlauf")
def add_benutzer(item: Dict[Any, Any]):
    szenario = item.get("szenario")
    absicht = item.get("absicht")
    eingabe = item.get("eingabe")
    ausgabe = item.get("ausgabe")
    note = item.get("note")
    klassifizierungsdatenbank = ModelTextklassifizierung()
    return {"result": klassifizierungsdatenbank.add_verlauf(szenario, absicht, eingabe, ausgabe, note)}

@app.post("/textklassifizierung/show_verlauf")
def add_benutzer():
    klassifizierungsdatenbank = ModelTextklassifizierung()
    return {"result": klassifizierungsdatenbank.show_verlauf()}

if __name__ == "__main__":
    uvicorn.run("main:app", host=api.TEXTKLASSIFIZIERUNG_SERVICE_IP, port=api.TEXTKLASSIFIZIERUNG_SERVICE_PORT)