import requests
""" import argparse

parser = argparse.ArgumentParser(description="Main-Server-Service")
parser.add_argument('--main_server_ip', type=str, required=True, help='Main-Server-Service IP')
parser.add_argument('--main_server_port', type=int, required=True, help='Main-Server-Service Port')
args = parser.parse_args() """
#############################################################################
MAIN_SERVER_SERVICE_IP = input("Main-Server-IP\t: ") #args.main_server_ip
MAIN_SERVER_SERVICE_PORT = input("Main-Server-Port: ") #args.main_server_port
#############################################################################


try:
    MAIN_SERVER_SERVICE_RESPONSE = requests.post(f"http://{MAIN_SERVER_SERVICE_IP}:{MAIN_SERVER_SERVICE_PORT}/main_server/config")

    if MAIN_SERVER_SERVICE_RESPONSE.status_code == 200:
        config_data = MAIN_SERVER_SERVICE_RESPONSE.json()
    else:
        raise FileNotFoundError(f"\nFehler beim Abrufen der MAIN-SERVER-CONFIG {MAIN_SERVER_SERVICE_RESPONSE.status_code}")
except Exception:
    raise FileNotFoundError(f"\n\n!!!Fehler beim Abrufen der MAIN-SERVER-CONFIG!!!")

AUDIO_SAMPLE_RATE = config_data['AUDIO_SAMPLE_RATE']

KONTOVERWALTUNG_SERVICE_IP = config_data['KONTOVERWALTUNG_SERVICE_IP']
KONTOVERWALTUNG_SERVICE_PORT = config_data['KONTOVERWALTUNG_SERVICE_PORT']

ANMERKUNG_THEMA = config_data['ANMERKUNG_THEMA']
ANMERKUNG_AKTIVITAET = config_data['ANMERKUNG_AKTIVITAET']
ANMERKUNG_ZEIT = config_data['ANMERKUNG_ZEIT']
ANMERKUNG_DATUM = config_data['ANMERKUNG_DATUM']
ANMERKUNG_ORT = config_data['ANMERKUNG_ORT']

ABSICHT_ABFRAGEN = config_data['ABSICHT_ABFRAGEN']
ABSICHT_EINGEBEN = config_data['ABSICHT_EINGEBEN']
ABSICHT_ENTFERNEN = config_data['ABSICHT_ENTFERNEN']
ABSICHT_ZURUECKGEHEN = config_data['ABSICHT_ZURUECKGEHEN']
ABSICHT_WEITERGEHEN = config_data['ABSICHT_WEITERGEHEN']
ABSICHT_WIEDERHOLEN = config_data['ABSICHT_WIEDERHOLEN']
ABSICHT_ABBRECHEN = config_data['ABSICHT_ABBRECHEN']
ABSICHT_WEITERGEHEN = config_data['ABSICHT_WEITERGEHEN']
ABSICHT_WEITERGEHEN = config_data['ABSICHT_WEITERGEHEN']

SZENARIO_UHRZEIT = config_data['SZENARIO_UHRZEIT']
SZENARIO_DATUM = config_data['SZENARIO_DATUM']
SZENARIO_WETTER = config_data['SZENARIO_WETTER']
SZENARIO_STUDIENORDNUNG = config_data['SZENARIO_STUDIENORDNUNG']
SZENARIO_WIKIPEDIA = config_data['SZENARIO_WIKIPEDIA']
SZENARIO_SYSTEM = config_data['SZENARIO_SYSTEM']
SZENARIO_TODO_LIST = config_data['SZENARIO_TODO_LIST']
SZENARIO_YOUTUBE = config_data['SZENARIO_YOUTUBE']
SZENARIO_SEARCH_ENGINE = config_data['SZENARIO_SEARCH_ENGINE']

ERROR_VARIABLE_ORT = config_data['ERROR_VARIABLE_ORT']
ERROR_VARIABLE_DATUM = config_data['ERROR_VARIABLE_DATUM']
ERROR_VARIABLE_ZEIT = config_data['ERROR_VARIABLE_ZEIT']
ERROR_VARIABLE_AKTIVITAET = config_data['ERROR_VARIABLE_AKTIVITAET']
ERROR_VARIABLE_THEMA = config_data['ERROR_VARIABLE_THEMA']

UHRZEIT_INTENT_SERVICE_IP = config_data['UHRZEIT_INTENT_SERVICE_IP']
UHRZEIT_INTENT_SERVICE_PORT = config_data['UHRZEIT_INTENT_SERVICE_PORT']
DATUM_INTENT_SERVICE_IP = config_data['DATUM_INTENT_SERVICE_IP']
DATUM_INTENT_SERVICE_PORT = config_data['DATUM_INTENT_SERVICE_PORT']
WETTER_INTENT_SERVICE_IP = config_data['WETTER_INTENT_SERVICE_IP']
WETTER_INTENT_SERVICE_PORT = config_data['WETTER_INTENT_SERVICE_PORT']
STUDIENORDNUNG_INTENT_SERVICE_IP = config_data['STUDIENORDNUNG_INTENT_SERVICE_IP']
STUDIENORDNUNG_INTENT_SERVICE_PORT = config_data['STUDIENORDNUNG_INTENT_SERVICE_PORT']
WIKIPEDIA_INTENT_SERVICE_IP = config_data['WIKIPEDIA_INTENT_SERVICE_IP']
WIKIPEDIA_INTENT_SERVICE_PORT = config_data['WIKIPEDIA_INTENT_SERVICE_PORT']
TODOLIST_INTENT_SERVICE_IP = config_data['TODOLIST_INTENT_SERVICE_IP']
TODOLIST_INTENT_SERVICE_PORT = config_data['TODOLIST_INTENT_SERVICE_PORT']

SPEECH_TO_TEXT_SERVICE_IP = config_data['SPEECH_TO_TEXT_SERVICE_IP']
SPEECH_TO_TEXT_SERVICE_PORT = config_data['SPEECH_TO_TEXT_SERVICE_PORT']
TEXT_TO_SPEECH_SERVICE_IP = config_data['TEXT_TO_SPEECH_SERVICE_IP']
TEXT_TO_SPEECH_SERVICE_PORT = config_data['TEXT_TO_SPEECH_SERVICE_PORT']
TEXTKLASSIFIZIERUNG_SERVICE_IP = config_data['TEXTKLASSIFIZIERUNG_SERVICE_IP']
TEXTKLASSIFIZIERUNG_SERVICE_PORT = config_data['TEXTKLASSIFIZIERUNG_SERVICE_PORT']
YOUTUBE_INTENT_SERVICE_IP = config_data['YOUTUBE_INTENT_SERVICE_IP']
YOUTUBE_INTENT_SERVICE_PORT = config_data['YOUTUBE_INTENT_SERVICE_PORT']
SEARCH_ENGINE_INTENT_SERVICE_IP = config_data['SEARCH_ENGINE_INTENT_SERVICE_IP']
SEARCH_ENGINE_INTENT_SERVICE_PORT = config_data['SEARCH_ENGINE_INTENT_SERVICE_PORT']

def authentifizierung(i_signal):
    try:
        i_signal = i_signal.tolist()
        response = requests.post(f"http://{KONTOVERWALTUNG_SERVICE_IP}:{KONTOVERWALTUNG_SERVICE_PORT}/kontoverwaltung/authentifizierung", json=i_signal)

        if response.status_code == 200:
            result = response.json()        
            return result, None
        else:
            return f"Error: {response.status_code}", 1
    except requests.ConnectionError:
        return "Fehler: Verbindung zum Server fehlgeschlagen. Bitte prüfen Sie den Serverstatus.", 1
    except requests.Timeout:
        return "Fehler: Die Anfrage hat zu lange gedauert. Bitte versuchen Sie es später erneut.", 1
    except Exception as e:
        return f"Ein unerwarteter Fehler ist aufgetreten: {e}", 1
    
def show_benutzer_name(i_benutzer_id):
    try:
        response = requests.post(f"http://{KONTOVERWALTUNG_SERVICE_IP}:{KONTOVERWALTUNG_SERVICE_PORT}/kontoverwaltung/show_benutzer_name", json=i_benutzer_id)

        if response.status_code == 200:
            result = response.json()
            
            name = result["result"]
            
            return name, None
        else:
            return f"Error: {response.status_code}", 1
    except requests.ConnectionError:
        return "Fehler: Verbindung zum Server fehlgeschlagen. Bitte prüfen Sie den Serverstatus.", 1
    except requests.Timeout:
        return "Fehler: Die Anfrage hat zu lange gedauert. Bitte versuchen Sie es später erneut.", 1
    except Exception as e:
        return f"Ein unerwarteter Fehler ist aufgetreten: {e}", 1
    
def add_benutzer(i_name):
    try:
        response = requests.post(f"http://{KONTOVERWALTUNG_SERVICE_IP}:{KONTOVERWALTUNG_SERVICE_PORT}/kontoverwaltung/add_benutzer", json=i_name)

        if response.status_code == 200:
            result = response.json()
            
            benutzer_id = result["result"]
            
            return benutzer_id, None
        else:
            return f"Error: {response.status_code}", 1
    except requests.ConnectionError:
        return "Fehler: Verbindung zum Server fehlgeschlagen. Bitte prüfen Sie den Serverstatus.", 1
    except requests.Timeout:
        return "Fehler: Die Anfrage hat zu lange gedauert. Bitte versuchen Sie es später erneut.", 1
    except Exception as e:
        return f"Ein unerwarteter Fehler ist aufgetreten: {e}", 1
    
def save_features(i_antwort_signal_trim, i_benutzer_id):
    try:
        i_antwort_signal_trim = i_antwort_signal_trim.tolist()
        response = requests.post(f"http://{KONTOVERWALTUNG_SERVICE_IP}:{KONTOVERWALTUNG_SERVICE_PORT}/kontoverwaltung/save_features", json={"signal":i_antwort_signal_trim, "benutzer_id": i_benutzer_id})

        if response.status_code == 200:
            result = response.json()        
            return result, None
        else:
            return f"Error: {response.status_code}", 1
    except requests.ConnectionError:
        return "Fehler: Verbindung zum Server fehlgeschlagen. Bitte prüfen Sie den Serverstatus.", 1
    except requests.Timeout:
        return "Fehler: Die Anfrage hat zu lange gedauert. Bitte versuchen Sie es später erneut.", 1
    except Exception as e:
        return f"Ein unerwarteter Fehler ist aufgetreten: {e}", 1
    
""" def train_authentifizierung_ki():
    try:
        response = requests.post(f"http://{KONTOVERWALTUNG_SERVICE_IP}:{KONTOVERWALTUNG_SERVICE_PORT}/kontoverwaltung/train_authentifizierung_ki")

        if response.status_code == 200:
            result = response.json()        
            return result, None
        else:
            return f"Error: {response.status_code}", 1
    except requests.ConnectionError:
        return "Fehler: Verbindung zum Server fehlgeschlagen. Bitte prüfen Sie den Serverstatus.", 1
    except requests.Timeout:
        return "Fehler: Die Anfrage hat zu lange gedauert. Bitte versuchen Sie es später erneut.", 1
    except Exception as e:
        return f"Ein unerwarteter Fehler ist aufgetreten: {e}", 1 """
    
def predictor_text_predict(i_text):
    try:
        response = requests.post(f"http://{TEXTKLASSIFIZIERUNG_SERVICE_IP}:{TEXTKLASSIFIZIERUNG_SERVICE_PORT}/textklassifizierung/klassifizieren", json=i_text)

        if response.status_code == 200:
            result = response.json()
            return result, None
        else:
            return f"Error: {response.status_code}", 1
    except requests.ConnectionError:
        return "Fehler: Verbindung zum Server fehlgeschlagen. Bitte prüfen Sie den Serverstatus.", 1
    except requests.Timeout:
        return "Fehler: Die Anfrage hat zu lange gedauert. Bitte versuchen Sie es später erneut.", 1
    except Exception as e:
        return f"Ein unerwarteter Fehler ist aufgetreten: {e}", 1


def uhrzeit_intent_abfragen(i_ort):
    try:
        response = requests.post(f"http://{UHRZEIT_INTENT_SERVICE_IP}:{UHRZEIT_INTENT_SERVICE_PORT}/uhrzeit_intent/abfragen", json=i_ort)

        if response.status_code == 200:
            result, error = response.json()        
            return result, error
        else:
            return f"Error: {response.status_code}", None
    except requests.ConnectionError:
        return "Fehler: Verbindung zum Server fehlgeschlagen. Bitte prüfen Sie den Serverstatus.", None
    except requests.Timeout:
        return "Fehler: Die Anfrage hat zu lange gedauert. Bitte versuchen Sie es später erneut.", None
    except Exception as e:
        return f"Ein unerwarteter Fehler ist aufgetreten: {e}", None
    
def datum_intent_abfragen(i_datum):
    try:
        response = requests.post(f"http://{DATUM_INTENT_SERVICE_IP}:{DATUM_INTENT_SERVICE_PORT}/datum_intent/abfragen", json=i_datum)

        if response.status_code == 200:
            result, error = response.json()        
            return result, error
        else:
            return f"Error: {response.status_code}", None
    except requests.ConnectionError:
        return "Fehler: Verbindung zum Server fehlgeschlagen. Bitte prüfen Sie den Serverstatus.", None
    except requests.Timeout:
        return "Fehler: Die Anfrage hat zu lange gedauert. Bitte versuchen Sie es später erneut.", None
    except Exception as e:
        return f"Ein unerwarteter Fehler ist aufgetreten: {e}", None
    
def wetter_intent_abfragen(i_zeit, i_datum, i_ort):
    try:
        response = requests.post(f"http://{WETTER_INTENT_SERVICE_IP}:{WETTER_INTENT_SERVICE_PORT}/wetter_intent/abfragen", json={"zeit":i_zeit, "datum":i_datum, "ort":i_ort})

        if response.status_code == 200:
            result, error = response.json()        
            return result, error
        else:
            return f"Error: {response.status_code}", None
    except requests.ConnectionError:
        return "Fehler: Verbindung zum Server fehlgeschlagen. Bitte prüfen Sie den Serverstatus.", None
    except requests.Timeout:
        return "Fehler: Die Anfrage hat zu lange gedauert. Bitte versuchen Sie es später erneut.", None
    except Exception as e:
        return f"Ein unerwarteter Fehler ist aufgetreten: {e}", None
    
def studienordnung_intent_abfragen(i_satz):
    try:
        response = requests.post(f"http://{STUDIENORDNUNG_INTENT_SERVICE_IP}:{STUDIENORDNUNG_INTENT_SERVICE_PORT}/studienordnung_intent/abfragen", json=i_satz)

        if response.status_code == 200:
            result, error = response.json()        
            return result, error
        else:
            return f"Error: {response.status_code}", None
    except requests.ConnectionError:
        return "Fehler: Verbindung zum Server fehlgeschlagen. Bitte prüfen Sie den Serverstatus.", None
    except requests.Timeout:
        return "Fehler: Die Anfrage hat zu lange gedauert. Bitte versuchen Sie es später erneut.", None
    except Exception as e:
        return f"Ein unerwarteter Fehler ist aufgetreten: {e}", None
    
def wikipedia_intent_abfragen(i_thema):
    try:
        response = requests.post(f"http://{WIKIPEDIA_INTENT_SERVICE_IP}:{WIKIPEDIA_INTENT_SERVICE_PORT}/wikipedia_intent/abfragen", json=i_thema)

        if response.status_code == 200:
            result, error = response.json()        
            return result, error
        else:
            return f"Error: {response.status_code}", None
    except requests.ConnectionError:
        return "Fehler: Verbindung zum Server fehlgeschlagen. Bitte prüfen Sie den Serverstatus.", None
    except requests.Timeout:
        return "Fehler: Die Anfrage hat zu lange gedauert. Bitte versuchen Sie es später erneut.", None
    except Exception as e:
        return f"Ein unerwarteter Fehler ist aufgetreten: {e}", None
    
def todolist_intent_abfragen(i_aktivitaet, i_zeit, i_datum, i_benutzer_id):
    try:
        response = requests.post(f"http://{TODOLIST_INTENT_SERVICE_IP}:{TODOLIST_INTENT_SERVICE_PORT}/todolist_intent/abfragen", json={"aktivitaet":i_aktivitaet, "zeit":i_zeit, "datum":i_datum, "benutzer_id":i_benutzer_id})

        if response.status_code == 200:
            result, error = response.json()        
            return result, error
        else:
            return f"Error: {response.status_code}", None
    except requests.ConnectionError:
        return "Fehler: Verbindung zum Server fehlgeschlagen. Bitte prüfen Sie den Serverstatus.", None
    except requests.Timeout:
        return "Fehler: Die Anfrage hat zu lange gedauert. Bitte versuchen Sie es später erneut.", None
    except Exception as e:
        return f"Ein unerwarteter Fehler ist aufgetreten: {e}", None
    
def todolist_intent_eingeben(i_aktivitaet, i_zeit, i_datum, i_benutzer_id):
    try:
        response = requests.post(f"http://{TODOLIST_INTENT_SERVICE_IP}:{TODOLIST_INTENT_SERVICE_PORT}/todolist_intent/eingeben", json={"aktivitaet":i_aktivitaet, "zeit":i_zeit, "datum":i_datum, "benutzer_id":i_benutzer_id})

        if response.status_code == 200:
            result, error = response.json()        
            return result, error
        else:
            return f"Error: {response.status_code}", None
    except requests.ConnectionError:
        return "Fehler: Verbindung zum Server fehlgeschlagen. Bitte prüfen Sie den Serverstatus.", None
    except requests.Timeout:
        return "Fehler: Die Anfrage hat zu lange gedauert. Bitte versuchen Sie es später erneut.", None
    except Exception as e:
        return f"Ein unerwarteter Fehler ist aufgetreten: {e}", None
    
def todolist_intent_eingeben(i_aktivitaet, i_zeit, i_datum, i_benutzer_id):
    try:
        response = requests.post(f"http://{TODOLIST_INTENT_SERVICE_IP}:{TODOLIST_INTENT_SERVICE_PORT}/todolist_intent/eingeben", json={"aktivitaet":i_aktivitaet, "zeit":i_zeit, "datum":i_datum, "benutzer_id":i_benutzer_id})

        if response.status_code == 200:
            result, error = response.json()        
            return result, error
        else:
            return f"Error: {response.status_code}", None
    except requests.ConnectionError:
        return "Fehler: Verbindung zum Server fehlgeschlagen. Bitte prüfen Sie den Serverstatus.", None
    except requests.Timeout:
        return "Fehler: Die Anfrage hat zu lange gedauert. Bitte versuchen Sie es später erneut.", None
    except Exception as e:
        return f"Ein unerwarteter Fehler ist aufgetreten: {e}", None
    
def todolist_intent_entfernen(i_aktivitaet, i_zeit, i_datum, i_benutzer_id):
    try:
        response = requests.post(f"http://{TODOLIST_INTENT_SERVICE_IP}:{TODOLIST_INTENT_SERVICE_PORT}/todolist_intent/entfernen", json={"aktivitaet":i_aktivitaet, "zeit":i_zeit, "datum":i_datum, "benutzer_id":i_benutzer_id})

        if response.status_code == 200:
            result, error = response.json()        
            return result, error
        else:
            return f"Error: {response.status_code}", None
    except requests.ConnectionError:
        return "Fehler: Verbindung zum Server fehlgeschlagen. Bitte prüfen Sie den Serverstatus.", None
    except requests.Timeout:
        return "Fehler: Die Anfrage hat zu lange gedauert. Bitte versuchen Sie es später erneut.", None
    except Exception as e:
        return f"Ein unerwarteter Fehler ist aufgetreten: {e}", None
    
def youtube_intent_abfragen(i_thema):
    try:
        response = requests.post(f"http://{YOUTUBE_INTENT_SERVICE_IP}:{YOUTUBE_INTENT_SERVICE_PORT}/youtube_intent/abfragen", json=i_thema)

        if response.status_code == 200:
            result, error, error_request = response.json()        
            return result, error, error_request
        else:
            return f"Error: {response.status_code}", None, 1
    except requests.ConnectionError:
        return "Fehler: Verbindung zum Server fehlgeschlagen. Bitte prüfen Sie den Serverstatus.", None, 1
    except requests.Timeout:
        return "Fehler: Die Anfrage hat zu lange gedauert. Bitte versuchen Sie es später erneut.", None, 1
    except Exception as e:
        return f"Ein unerwarteter Fehler ist aufgetreten: {e}", None, 1

def search_engine_intent_abfragen(i_thema):
    try:
        response = requests.post(f"http://{SEARCH_ENGINE_INTENT_SERVICE_IP}:{SEARCH_ENGINE_INTENT_SERVICE_PORT}/search_engine_intent/abfragen", json=i_thema)

        if response.status_code == 200:
            result, error, error_request = response.json()        
            return result, error, error_request
        else:
            return f"Error: {response.status_code}", None, 1
    except requests.ConnectionError:
        return "Fehler: Verbindung zum Server fehlgeschlagen. Bitte prüfen Sie den Serverstatus.", None, 1
    except requests.Timeout:
        return "Fehler: Die Anfrage hat zu lange gedauert. Bitte versuchen Sie es später erneut.", None, 1
    except Exception as e:
        return f"Ein unerwarteter Fehler ist aufgetreten: {e}", None, 1
    
def speech_to_text_recognize(i_signal):
    try:
        i_signal = i_signal.tolist()
        response = requests.post(f"http://{SPEECH_TO_TEXT_SERVICE_IP}:{SPEECH_TO_TEXT_SERVICE_PORT}/speech_to_text/recognize", json=i_signal)

        if response.status_code == 200:
            result = response.json()
            return result["result"], None
        else:
            return f"Error: {response.status_code}", 1
    except requests.ConnectionError:
        return "Fehler: Verbindung zum Server fehlgeschlagen. Bitte prüfen Sie den Serverstatus.", 1
    except requests.Timeout:
        return "Fehler: Die Anfrage hat zu lange gedauert. Bitte versuchen Sie es später erneut.", 1
    except Exception as e:
        return f"Ein unerwarteter Fehler ist aufgetreten: {e}", 1
    
def text_to_speech_generieren(i_text):
    try:
        response = requests.post(f"http://{TEXT_TO_SPEECH_SERVICE_IP}:{TEXT_TO_SPEECH_SERVICE_PORT}/text_to_speech/generieren", json=i_text)

        if response.status_code == 200:
            result = response.json()        
            return result["result"], None
        else:
            return f"Error: {response.status_code}", 1
    except requests.ConnectionError:
        return "Fehler: Verbindung zum Server fehlgeschlagen. Bitte prüfen Sie den Serverstatus.", 1
    except requests.Timeout:
        return "Fehler: Die Anfrage hat zu lange gedauert. Bitte versuchen Sie es später erneut.", 1
    except Exception as e:
        return f"Ein unerwarteter Fehler ist aufgetreten: {e}", 1
    
def add_verlauf(i_szenario, i_absicht, i_eingabe, i_ausgabe, i_note):
    try:
        response = requests.post(f"http://{TEXTKLASSIFIZIERUNG_SERVICE_IP}:{TEXTKLASSIFIZIERUNG_SERVICE_PORT}/textklassifizierung/add_verlauf", json={"szenario":i_szenario, "absicht": i_absicht, "eingabe": i_eingabe, "ausgabe": i_ausgabe, "note": i_note})

        if response.status_code == 200:
            result = response.json()
            return result["result"] if result["result"] else "Server Error!", None if result["result"] else 1
        else:
            return f"Error: {response.status_code}", 1
    except requests.ConnectionError:
        return "Fehler: Verbindung zum Server fehlgeschlagen. Bitte prüfen Sie den Serverstatus.", 1
    except requests.Timeout:
        return "Fehler: Die Anfrage hat zu lange gedauert. Bitte versuchen Sie es später erneut.", 1
    except Exception as e:
        return f"Ein unerwarteter Fehler ist aufgetreten: {e}", 1
    
def show_verlauf():
    try:
        response = requests.post(f"http://{TEXTKLASSIFIZIERUNG_SERVICE_IP}:{TEXTKLASSIFIZIERUNG_SERVICE_PORT}/textklassifizierung/show_verlauf")

        if response.status_code == 200:
            result = response.json()
            return result["result"], None
        else:
            return f"Error: {response.status_code}", 1
    except requests.ConnectionError:
        return "Fehler: Verbindung zum Server fehlgeschlagen. Bitte prüfen Sie den Serverstatus.", 1
    except requests.Timeout:
        return "Fehler: Die Anfrage hat zu lange gedauert. Bitte versuchen Sie es später erneut.", 1
    except Exception as e:
        return f"Ein unerwarteter Fehler ist aufgetreten: {e}", 1
    
def delete_verlauf(verlauf_id):
    try:
        response = requests.post(f"http://{TEXTKLASSIFIZIERUNG_SERVICE_IP}:{TEXTKLASSIFIZIERUNG_SERVICE_PORT}/textklassifizierung/delete_verlauf", json=verlauf_id)

        if response.status_code == 200:
            result = response.json()
            delete_result, delete_error = result["result"]
            return delete_result, delete_error, None
        else:
            return f"Error: {response.status_code}", 1
    except requests.ConnectionError:
        return "Fehler: Verbindung zum Server fehlgeschlagen. Bitte prüfen Sie den Serverstatus.", None, 1
    except requests.Timeout:
        return "Fehler: Die Anfrage hat zu lange gedauert. Bitte versuchen Sie es später erneut.", None, 1
    except Exception as e:
        return f"Ein unerwarteter Fehler ist aufgetreten: {e}", None, 1