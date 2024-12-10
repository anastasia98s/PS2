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
        raise FileNotFoundError(f"\nFehler beim Abrufen der MAIN-SERVER-CONFIG {MAIN_SERVER_SERVICE_RESPONSE.status_code}")
except Exception:
    raise FileNotFoundError(f"\n\n!!!Fehler beim Abrufen der MAIN-SERVER-CONFIG!!!")

YOUTUBE_INTENT_SERVICE_IP = config_data['YOUTUBE_INTENT_SERVICE_IP']
YOUTUBE_INTENT_SERVICE_PORT = config_data['YOUTUBE_INTENT_SERVICE_PORT']
ERROR_VARIABLE_THEMA = config_data['ERROR_VARIABLE_THEMA']

def web_indexing(url):
    try:
        response = requests.post(f"http://{MAIN_SERVER_SERVICE_IP}:{MAIN_SERVER_SERVICE_PORT}/main_server/web_indexing", json=url)

        if response.status_code == 200:
            result = response.json()
            return result["result"], result["error_indexing"], None
        else:
            return f"Error: {response.status_code}", None, 1
    except Exception:
        return "Fehler: Anfrage konnte nicht verarbeitet werden", None, 1