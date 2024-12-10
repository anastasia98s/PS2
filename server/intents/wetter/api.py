import requests
import argparse

parser = argparse.ArgumentParser(description="Shared-Data-Service (Server)")
parser.add_argument('--ip', type=str, required=True, help='Shared-Data-Service IP')
parser.add_argument('--port', type=int, required=True, help='Shared-Data-Service Port')
args = parser.parse_args()
#############################################################################
SHARED_DATA_SERVICE_IP = args.ip
SHARED_DATA_SERVICE_PORT = args.port
#############################################################################
shared_data = None

try:
    SHARED_SERVICE_RESPONSE = requests.post(f"http://{SHARED_DATA_SERVICE_IP}:{SHARED_DATA_SERVICE_PORT}/shared_data/config")
    if SHARED_SERVICE_RESPONSE.status_code == 200:
        config_data = SHARED_SERVICE_RESPONSE.json()
    else:
        raise FileNotFoundError(f"\nFehler beim Abrufen der SHARED-CONFIG {SHARED_SERVICE_RESPONSE.status_code}")
except Exception:
    raise FileNotFoundError(f"\n\n!!!Fehler beim Abrufen der SHARED-CONFIG!!!")

WETTER_INTENT_SERVICE_IP = config_data['WETTER_INTENT_SERVICE_IP']
WETTER_INTENT_SERVICE_PORT = config_data['WETTER_INTENT_SERVICE_PORT']
ERROR_VARIABLE_ORT = config_data['ERROR_VARIABLE_ORT']

def date_zeit_text_cleaner(i_text, is_zeit=False):
    try:
        response = requests.post(f"http://{SHARED_DATA_SERVICE_IP}:{SHARED_DATA_SERVICE_PORT}/shared_data/date_zeit_text_cleaner", json={"text": i_text, "is_zeit": is_zeit})

        if response.status_code == 200:
            result = response.json()
            
            clean_text = result["result"]
            
            return clean_text, None
        else:
            return f"Error: {response.status_code}", 1
    except Exception:
        return "Fehler: Anfrage konnte nicht verarbeitet werden", 1

def date_zeit_konverter(i_datum, i_zeit):
    try:
        response = requests.post(f"http://{SHARED_DATA_SERVICE_IP}:{SHARED_DATA_SERVICE_PORT}/shared_data/date_zeit_konverter", json={"datum": i_datum, "zeit": i_zeit})

        if response.status_code == 200:
            result = response.json()
            
            datezeit = result["result"]
            error = result["error"]
            
            return datezeit, error, None
        else:
            return f"Error: {response.status_code}", None, 1
    except Exception:
        return "Fehler: Anfrage konnte nicht verarbeitet werden", None, 1

def date_konverter(i_datum):
    try:
        response = requests.post(f"http://{SHARED_DATA_SERVICE_IP}:{SHARED_DATA_SERVICE_PORT}/shared_data/date_konverter", json=i_datum)

        if response.status_code == 200:
            result = response.json()
            
            datum = result["result"]
            error = result["error"]
            
            return datum, error, None
        else:
            return f"Error: {response.status_code}", None, 1
    except Exception:
        return "Fehler: Anfrage konnte nicht verarbeitet werden", None, 1

def date_text_konverter(i_datum):
    try:
        response = requests.post(f"http://{SHARED_DATA_SERVICE_IP}:{SHARED_DATA_SERVICE_PORT}/shared_data/date_text_konverter", json=i_datum)

        if response.status_code == 200:
            result = response.json()
            
            datum = result["result"]
            
            return datum, None
        else:
            return f"Error: {response.status_code}", 1
    except Exception:
        return "Fehler: Anfrage konnte nicht verarbeitet werden", 1

def zeit_text_konverter(i_zeit):
    try:
        response = requests.post(f"http://{SHARED_DATA_SERVICE_IP}:{SHARED_DATA_SERVICE_PORT}/shared_data/zeit_text_konverter", json=i_zeit)

        if response.status_code == 200:
            result = response.json()
            
            zeit = result["result"]

            return zeit, None
        else:
            return f"Error: {response.status_code}", 1
    except Exception:
        return "Fehler: Anfrage konnte nicht verarbeitet werden", 1