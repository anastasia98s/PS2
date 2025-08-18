import api
from fastapi import FastAPI, Body
import uvicorn
from datetime import datetime

app = FastAPI()

@app.post("/datum_intent/abfragen")
def abfragen(i_datum: str = Body(...)): # Welches Datum ist morgen/heute/gestern/am Sonntag..
    i_datum, error_request = api.date_zeit_text_cleaner(i_datum)
    if error_request:
        return i_datum, None # error verbindung
    
    t_datum, errortyp, error_request = api.date_konverter(i_datum)
    if error_request:
        return t_datum, None
    if not t_datum:
        return None, errortyp # error variable
    
    t_datum = datetime.fromisoformat(t_datum)
    t_datum = t_datum.strftime("%d. %B %Y")

    text_datum, error_request = api.date_text_next_konverter(i_datum)
    if error_request:
        return text_datum, None
    
    return f"{text_datum} ist der {t_datum}", None # 200

if __name__ == "__main__":
    uvicorn.run("main:app", host=api.DATUM_INTENT_SERVICE_IP, port=api.DATUM_INTENT_SERVICE_PORT)