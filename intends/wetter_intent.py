import requests
import config

class WetterIntent:
    def __init__(self):
        pass
    
    # Override
    def abfragen(self, i_zeit, i_datum, i_ort): # Bsp. Wie ist das Wetter um 18 Uhr morgen in Berlin
        #url = f"http://example.com/weather?date={i_datum}&time={i_zeit}&location={i_ort}" # such ein besseres API
        if not i_ort:
            i_ort = config.DEFAULT_ORT
        bedingung_url = f"http://wttr.in/{i_ort}?format=%C&lang=de"
        temperatur_url = f"http://wttr.in/{i_ort}?format=%t"
        bedingung_response = requests.get(bedingung_url)
        temperatur_response = requests.get(temperatur_url)
        if bedingung_response.status_code == 200 and temperatur_response.status_code == 200:
            bedingung = bedingung_response.text.strip()
            temperatur = temperatur_response.text.strip()
            temperatur = ''.join(filter(str.isdigit, temperatur))
            return f"in {i_ort} {i_datum} {i_zeit} {bedingung} {temperatur} Grad"
        else:
            return "Wetter Error"