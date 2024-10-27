import requests

class WetterIntent:
    def __init__(self):
        pass

    def abfragen(self, i_zeit, i_datum, i_ort):
        #url = f"http://example.com/weather?date={i_datum}&time={i_zeit}&location={i_ort}" # such ein besseres API

        bedingung_url = f"http://wttr.in/{i_ort}?format=%C&lang=de"
        temperatur_url = f"http://wttr.in/{i_ort}?format=%t"
        bedingung_response = requests.get(bedingung_url)
        temperatur_response = requests.get(temperatur_url)
        if bedingung_response.status_code == 200 and temperatur_response.status_code == 200:
            bedingung = bedingung_response.text.strip()
            temperatur = temperatur_response.text.strip()
            temperatur = ''.join(filter(str.isdigit, temperatur))
            return f"in {i_ort} {bedingung} {temperatur} Grad"
        else:
            return "Wetter Error"