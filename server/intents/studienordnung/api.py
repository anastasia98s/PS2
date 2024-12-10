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

STUDIENORDNUNG_INTENT_SERVICE_IP = config_data['STUDIENORDNUNG_INTENT_SERVICE_IP']
STUDIENORDNUNG_INTENT_SERVICE_PORT = config_data['STUDIENORDNUNG_INTENT_SERVICE_PORT']