import api
from fastapi import FastAPI, Body
import uvicorn
from datetime import datetime

app = FastAPI()

@app.post("/datum_intent/abfragen")
def abfragen(i_datum: str = Body(...)): # Welches Datum ist morgen/heute/gestern/am Sonntag..
    datum, errortyp, error_request = api.date_konverter(i_datum)
    if error_request:
        return datum, None # error verbindung
    
    if not datum:
        return None, errortyp # error variable
    datum = datetime.fromisoformat(datum)
    datum = datum.strftime("%d. %B %Y")
    return f"{i_datum} ist der {datum}", None # 200

if __name__ == "__main__":
    uvicorn.run("main:app", host=api.DATUM_INTENT_SERVICE_IP, port=api.DATUM_INTENT_SERVICE_PORT)