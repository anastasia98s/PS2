import api
from fastapi import FastAPI
from typing import Dict, Any
import uvicorn
import requests
import config
from datetime import datetime

app = FastAPI()

@app.post("/wetter_intent/abfragen") 
def abfragen(item: Dict[Any, Any]): # Bsp. Wie ist das Wetter um 18 Uhr morgen in Berlin
    i_zeit = item.get("zeit")
    i_datum = item.get("datum")
    i_ort = item.get("ort")
    #url = f"http://example.com/weather?date={i_datum}&time={i_zeit}&location={i_ort}" # such ein besseres API
    
    if not i_ort:
        i_ort = config.DEFAULT_ORT

    try:
        if i_datum or i_zeit:
            if not i_datum:
                i_datum = config.DEFAULT_DATUM
            
            i_datum, error_request = api.date_zeit_text_cleaner(i_datum)
            if error_request:
                return i_datum, None
            if i_zeit:
                i_zeit, error_request = api.date_zeit_text_cleaner(i_zeit, is_zeit=True)
                if error_request:
                    return i_zeit, None
                datezeit, errortyp, error_request = api.date_zeit_konverter(i_datum, i_zeit) # Die API kann derzeit an bestimmten Tagen keine Abfragen durchführen
                if error_request:
                    return datezeit, None
                if not datezeit:
                    return None, errortyp
                
                # datum + uhrzeit
                bedingung_url = f"http://wttr.in/{i_ort}?format=%C&lang=de"
                temperatur_url = f"http://wttr.in/{i_ort}?format=%t"

            else:
                datum, errortyp, error_request = api.date_konverter(i_datum) # API Die API kann derzeit an bestimmten Tagen keine Abfragen durchführen
                if error_request:
                    return datum, None
                if not datum:
                    return None, errortyp
                else:
                    datum = datetime.fromisoformat(datum)
                    datum = datum.strftime("%Y-%m-%d")
                
                # datum
                bedingung_url = f"http://wttr.in/{i_ort}?format=%C&lang=de"
                temperatur_url = f"http://wttr.in/{i_ort}?format=%t"
        else:
            # jetzt
            bedingung_url = f"http://wttr.in/{i_ort}?format=%C&lang=de"
            temperatur_url = f"http://wttr.in/{i_ort}?format=%t"

        bedingung_response = requests.get(bedingung_url)
        temperatur_response = requests.get(temperatur_url)
        if bedingung_response.status_code == 200 and temperatur_response.status_code == 200:
            bedingung = bedingung_response.text.strip()
            temperatur = temperatur_response.text.strip()
            temperatur = ''.join(filter(str.isdigit, temperatur))
            
            if i_datum:
                i_datum, error_request = api.date_text_konverter(i_datum)
                if error_request:
                    return i_datum, None
            else:
                i_datum = ""
                
            if i_zeit:
                i_zeit, error_request = api.zeit_text_konverter(i_zeit)
                if error_request:
                    return i_zeit, None
            else:
                i_zeit = ""
            return f"in {i_ort} ist es {i_datum} {i_zeit} {bedingung} bei {temperatur} Grad", None
        else:
            return None, api.ERROR_VARIABLE_ORT
    except Exception as e:
        return "Bei der Wetterabfrage ist ein Fehler aufgetreten", None
    
if __name__ == "__main__":
    uvicorn.run("main:app", host=api.WETTER_INTENT_SERVICE_IP, port=api.WETTER_INTENT_SERVICE_PORT)