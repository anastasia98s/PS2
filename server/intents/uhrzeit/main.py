import api
from fastapi import FastAPI, Body
import uvicorn
from datetime import datetime
import pytz
import config

app = FastAPI()

@app.post("/uhrzeit_intent/abfragen")
def abfragen(i_ort: str = Body(...)):
    time = datetime.now(pytz.utc)
    if i_ort:
        if i_ort.lower() in config.TIMEZONE:
            timezone = pytz.timezone(config.TIMEZONE[i_ort.lower()])
            time = time.astimezone(timezone)
        else:
            return f"Leider wurde die Zeitzone für '{i_ort}' auf dem Server nicht festgelegt", None

        zeit = time.strftime("%H:%M")
        return f"In {i_ort} ist es jetzt um {zeit} Uhr", None
    else:
        zeit = time.strftime("%H:%M")
        return f"Jetzt ist es um {zeit} Uhr", None
    
if __name__ == "__main__":
    uvicorn.run("main:app", host=api.UHRZEIT_INTENT_SERVICE_IP, port=api.UHRZEIT_INTENT_SERVICE_PORT)