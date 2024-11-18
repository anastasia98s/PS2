import requests
import config
from intents.datenkonverter import Datenkonverter

class WetterIntent(Datenkonverter):
    def __init__(self):
        super().__init__()
    
    def abfragen(self, i_zeit, i_datum, i_ort): # Bsp. Wie ist das Wetter um 18 Uhr morgen in Berlin
        #url = f"http://example.com/weather?date={i_datum}&time={i_zeit}&location={i_ort}" # such ein besseres API
                
        if not i_ort:
            i_ort = config.DEFAULT_ORT

        try:
            if i_datum:
                if i_zeit:
                    datezeit, errortyp = super().date_zeit_konverter(i_datum, i_zeit) # Die API kann derzeit an bestimmten Tagen keine Abfragen durchführen
                    if not datezeit:
                        return None, errortyp
                    bedingung_url = f"http://wttr.in/{i_ort}?format=%C&lang=de"
                    temperatur_url = f"http://wttr.in/{i_ort}?format=%t"
                else:
                    datum, errortyp = super().date_konverter(i_datum) # API Die API kann derzeit an bestimmten Tagen keine Abfragen durchführen
                    if not datum:
                        return None, errortyp
                    else:
                        datum = datum.strftime("%Y-%m-%d")
                        
                    bedingung_url = f"http://wttr.in/{i_ort}?format=%C&lang=de"
                    temperatur_url = f"http://wttr.in/{i_ort}?format=%t"
            else:
                bedingung_url = f"http://wttr.in/{i_ort}?format=%C&lang=de"
                temperatur_url = f"http://wttr.in/{i_ort}?format=%t"

            bedingung_response = requests.get(bedingung_url)
            temperatur_response = requests.get(temperatur_url)
            if bedingung_response.status_code == 200 and temperatur_response.status_code == 200:
                bedingung = bedingung_response.text.strip()
                temperatur = temperatur_response.text.strip()
                temperatur = ''.join(filter(str.isdigit, temperatur))
                return f"in {i_ort} {i_datum} {i_zeit} {bedingung} {temperatur} Grad", None
            else:
                return None, config.ERROR_VARIABLE_ORT
        except Exception as e:
            return "Bei der Wetterabfrage ist ein Fehler aufgetreten", None