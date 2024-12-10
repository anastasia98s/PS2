from fastapi import FastAPI, Body
from typing import Dict, Any
import config
import datenkonverter
import uvicorn

app = FastAPI()

@app.post("/shared_data/config")
def show_config():
    return {
        "DEVICE": str(config.DEVICE),
        "TEXTKLASSIFIZIERUNG_SERVICE_IP": config.TEXTKLASSIFIZIERUNG_SERVICE_IP,
        "TEXTKLASSIFIZIERUNG_SERVICE_PORT": config.TEXTKLASSIFIZIERUNG_SERVICE_PORT,
        "KONTOVERWALTUNG_SERVICE_IP": config.KONTOVERWALTUNG_SERVICE_IP,
        "KONTOVERWALTUNG_SERVICE_PORT": config.KONTOVERWALTUNG_SERVICE_PORT,
        "SPEECH_TO_TEXT_SERVICE_IP": config.SPEECH_TO_TEXT_SERVICE_IP,
        "SPEECH_TO_TEXT_SERVICE_PORT": config.SPEECH_TO_TEXT_SERVICE_PORT,
        "TEXT_TO_SPEECH_SERVICE_IP": config.TEXT_TO_SPEECH_SERVICE_IP,
        "TEXT_TO_SPEECH_SERVICE_PORT": config.TEXT_TO_SPEECH_SERVICE_PORT,
        "DATUM_INTENT_SERVICE_IP": config.DATUM_INTENT_SERVICE_IP,
        "DATUM_INTENT_SERVICE_PORT": config.DATUM_INTENT_SERVICE_PORT,
        "UHRZEIT_INTENT_SERVICE_IP": config.UHRZEIT_INTENT_SERVICE_IP,
        "UHRZEIT_INTENT_SERVICE_PORT": config.UHRZEIT_INTENT_SERVICE_PORT,
        "WETTER_INTENT_SERVICE_IP": config.WETTER_INTENT_SERVICE_IP,
        "WETTER_INTENT_SERVICE_PORT": config.WETTER_INTENT_SERVICE_PORT,
        "WIKIPEDIA_INTENT_SERVICE_IP": config.WIKIPEDIA_INTENT_SERVICE_IP,
        "WIKIPEDIA_INTENT_SERVICE_PORT": config.WIKIPEDIA_INTENT_SERVICE_PORT,
        "STUDIENORDNUNG_INTENT_SERVICE_IP": config.STUDIENORDNUNG_INTENT_SERVICE_IP,
        "STUDIENORDNUNG_INTENT_SERVICE_PORT": config.STUDIENORDNUNG_INTENT_SERVICE_PORT,
        "TODOLIST_INTENT_SERVICE_IP": config.TODOLIST_INTENT_SERVICE_IP,
        "TODOLIST_INTENT_SERVICE_PORT": config.TODOLIST_INTENT_SERVICE_PORT,
        "SEARCH_ENGINE_INTENT_SERVICE_IP": config.SEARCH_ENGINE_INTENT_SERVICE_IP,
        "SEARCH_ENGINE_INTENT_SERVICE_PORT": config.SEARCH_ENGINE_INTENT_SERVICE_PORT,
        "YOUTUBE_INTENT_SERVICE_IP": config.YOUTUBE_INTENT_SERVICE_IP,
        "YOUTUBE_INTENT_SERVICE_PORT": config.YOUTUBE_INTENT_SERVICE_PORT,
        "AUDIO_SAMPLE_RATE": config.AUDIO_SAMPLE_RATE,
        "ABSICHT_ABFRAGEN": config.ABSICHT_ABFRAGEN,
        "ABSICHT_EINGEBEN": config.ABSICHT_EINGEBEN,
        "ABSICHT_ENTFERNEN": config.ABSICHT_ENTFERNEN,
        "ABSICHT_ZURUECKGEHEN": config.ABSICHT_ZURUECKGEHEN,
        "ABSICHT_WEITERGEHEN": config.ABSICHT_WEITERGEHEN,
        "ABSICHT_WIEDERHOLEN": config.ABSICHT_WIEDERHOLEN,
        "ABSICHT_ABBRECHEN": config.ABSICHT_ABBRECHEN,
        "SZENARIO_WETTER": config.SZENARIO_WETTER,
        "SZENARIO_STUDIENORDNUNG": config.SZENARIO_STUDIENORDNUNG,
        "SZENARIO_WIKIPEDIA": config.SZENARIO_WIKIPEDIA,
        "SZENARIO_TODO_LIST": config.SZENARIO_TODO_LIST,
        "SZENARIO_UHRZEIT": config.SZENARIO_UHRZEIT,
        "SZENARIO_DATUM": config.SZENARIO_DATUM,
        "SZENARIO_SYSTEM": config.SZENARIO_SYSTEM,
        "SZENARIO_YOUTUBE": config.SZENARIO_YOUTUBE,
        "SZENARIO_SEARCH_ENGINE": config.SZENARIO_SEARCH_ENGINE,
        "ANMERKUNG_THEMA": config.ANMERKUNG_THEMA,
        "ANMERKUNG_AKTIVITAET": config.ANMERKUNG_AKTIVITAET,
        "ANMERKUNG_ZEIT": config.ANMERKUNG_ZEIT,
        "ANMERKUNG_DATUM": config.ANMERKUNG_DATUM,
        "ANMERKUNG_ORT": config.ANMERKUNG_ORT,
        "ERROR_VARIABLE_DATUM": config.ERROR_VARIABLE_DATUM,
        "ERROR_VARIABLE_ZEIT": config.ERROR_VARIABLE_ZEIT,
        "ERROR_VARIABLE_ORT": config.ERROR_VARIABLE_ORT,
        "ERROR_VARIABLE_AKTIVITAET": config.ERROR_VARIABLE_AKTIVITAET,
        "ERROR_VARIABLE_THEMA": config.ERROR_VARIABLE_THEMA,
    }

@app.post("/shared_data/date_konverter")
def date_konverter(datum: str = Body(...)):
    result, error = datenkonverter.date_konverter(datum)
    return {"result": result, "error": error}

@app.post("/shared_data/zeit_text_konverter")
def zeit_text_konverter(zeit: str = Body(...)):
    return {"result": datenkonverter.zeit_text_konverter(zeit)}

@app.post("/shared_data/date_text_konverter")
def date_text_konverter(datum: str = Body(...)):
    return {"result": datenkonverter.date_text_konverter(datum)}

@app.post("/shared_data/date_zeit_konverter")
def date_zeit_konverter(item: Dict[Any, Any]):
    datum = item.get("datum")
    zeit = item.get("zeit")
    result, error = datenkonverter.date_zeit_konverter(datum, zeit)
    return {"result": result, "error": error}

@app.post("/shared_data/date_zeit_text_cleaner")
def date_zeit_text_cleaner(item: Dict[Any, Any]):
    text = item.get("text")
    is_zeit = item.get("is_zeit") # false/true/none
    return {"result": datenkonverter.date_zeit_text_cleaner(text, is_zeit)}

@app.post("/shared_data/web_indexing")
def web_indexing(url: str = Body(...)):
    result, error = datenkonverter.web_indexing(url)
    return {"result": result, "error_indexing": error}

if __name__ == "__main__":
    uvicorn.run("main:app", host=config.SHARED_DATA_SERVICE_IP, port=config.SHARED_DATA_SERVICE_PORT)