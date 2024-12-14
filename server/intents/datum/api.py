import requests
import argparse

parser = argparse.ArgumentParser(description="Main-Server-Service")
parser.add_argument('--main_server_ip', type=str, required=True, help='Main-Server-Service IP')
parser.add_argument('--main_server_port', type=int, required=True, help='Main-Server-Service Port')
args = parser.parse_args()
#############################################################################
MAIN_SERVER_SERVICE_IP = args.main_server_ip
MAIN_SERVER_SERVICE_PORT = args.main_server_port
#############################################################################


try:
    MAIN_SERVER_SERVICE_RESPONSE = requests.post(f"http://{MAIN_SERVER_SERVICE_IP}:{MAIN_SERVER_SERVICE_PORT}/main_server/config")

    if MAIN_SERVER_SERVICE_RESPONSE.status_code == 200:
        config_data = MAIN_SERVER_SERVICE_RESPONSE.json()
    else:
        raise ConnectionError(f"\nFehler beim Abrufen der MAIN-SERVER-CONFIG {MAIN_SERVER_SERVICE_RESPONSE.status_code}")
except Exception:
    raise ConnectionError(f"\n\n!!!Fehler beim Abrufen der MAIN-SERVER-CONFIG!!!")

DATUM_INTENT_SERVICE_IP = config_data['DATUM_INTENT_SERVICE_IP']
DATUM_INTENT_SERVICE_PORT = config_data['DATUM_INTENT_SERVICE_PORT']

def date_konverter(i_datum):
    try:
        response = requests.post(f"http://{MAIN_SERVER_SERVICE_IP}:{MAIN_SERVER_SERVICE_PORT}/main_server/date_konverter", json=i_datum)

        if response.status_code == 200:
            result = response.json()
            
            datum = result["result"]
            error = result["error"]
            
            return datum, error, None
        else:
            return f"Error: {response.status_code}", None, 1
    except Exception:
        return "Fehler: Anfrage konnte nicht verarbeitet werden", None, 1