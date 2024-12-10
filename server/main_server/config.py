import argparse

parser = argparse.ArgumentParser(description="Main-Service")
parser.add_argument('--main_server_ip', type=str, required=True, help='Main-Service IP')
parser.add_argument('--main_server_port', type=int, required=True, help='Main-Service Port')
parser.add_argument('--textklassifizierung_ip', type=str, required=True, help='Textklassifizierung-Service IP')
parser.add_argument('--textklassifizierung_port', type=int, required=True, help='Textklassifizierung-Service Port')
parser.add_argument('--kontoverwaltung_ip', type=str, required=True, help='Kontoverwaltung-Service IP')
parser.add_argument('--kontoverwaltung_port', type=int, required=True, help='Kontoverwaltung-Service Port')
parser.add_argument('--speech_to_text_ip', type=str, required=True, help='Speech-to-Text-Service IP')
parser.add_argument('--speech_to_text_port', type=int, required=True, help='Speech-to-Text-Service Port')
parser.add_argument('--text_to_speech_ip', type=str, required=True, help='Text-to-Speech-Service IP')
parser.add_argument('--text_to_speech_port', type=int, required=True, help='Text-to-Speech-Service Port')
parser.add_argument('--datum_intent_ip', type=str, required=True, help='Datum-Intent-Service IP')
parser.add_argument('--datum_intent_port', type=int, required=True, help='Datum-Intent-Service Port')
parser.add_argument('--uhrzeit_intent_ip', type=str, required=True, help='Uhrzeit-Intent-Service IP')
parser.add_argument('--uhrzeit_intent_port', type=int, required=True, help='Uhrzeit-Intent-Service Port')
parser.add_argument('--wetter_intent_ip', type=str, required=True, help='Wetter-Intent-Service IP')
parser.add_argument('--wetter_intent_port', type=int, required=True, help='Wetter-Intent-Service Port')
parser.add_argument('--wikipedia_intent_ip', type=str, required=True, help='Wikipedia-Intent-Service IP')
parser.add_argument('--wikipedia_intent_port', type=int, required=True, help='Wikipedia-Intent-Service Port')
parser.add_argument('--studienordnung_intent_ip', type=str, required=True, help='Studienordnung-Intent-Service IP')
parser.add_argument('--studienordnung_intent_port', type=int, required=True, help='Studienordnung-Intent-Service Port')
parser.add_argument('--todolist_intent_ip', type=str, required=True, help='ToDoList-Intent-Service IP')
parser.add_argument('--todolist_intent_port', type=int, required=True, help='ToDoList-Intent-Service Port')
parser.add_argument('--search_engine_intent_ip', type=str, required=True, help='Search-Engine-Intent-Service IP')
parser.add_argument('--search_engine_intent_port', type=int, required=True, help='Search-Engine-Intent-Service Port')
parser.add_argument('--youtube_intent_ip', type=str, required=True, help='YouTube-Intent-Service IP')
parser.add_argument('--youtube_intent_port', type=int, required=True, help='YouTube-Intent-Service Port')

args = parser.parse_args()
#############################################################################
MAIN_SERVER_SERVICE_IP = args.main_server_ip
MAIN_SERVER_SERVICE_PORT = args.main_server_port

TEXTKLASSIFIZIERUNG_SERVICE_IP = args.textklassifizierung_ip
TEXTKLASSIFIZIERUNG_SERVICE_PORT = args.textklassifizierung_port

KONTOVERWALTUNG_SERVICE_IP = args.kontoverwaltung_ip
KONTOVERWALTUNG_SERVICE_PORT = args.kontoverwaltung_port

SPEECH_TO_TEXT_SERVICE_IP = args.speech_to_text_ip
SPEECH_TO_TEXT_SERVICE_PORT = args.speech_to_text_port

TEXT_TO_SPEECH_SERVICE_IP = args.text_to_speech_ip
TEXT_TO_SPEECH_SERVICE_PORT = args.text_to_speech_port

DATUM_INTENT_SERVICE_IP = args.datum_intent_ip
DATUM_INTENT_SERVICE_PORT = args.datum_intent_port

UHRZEIT_INTENT_SERVICE_IP = args.uhrzeit_intent_ip
UHRZEIT_INTENT_SERVICE_PORT = args.uhrzeit_intent_port

WETTER_INTENT_SERVICE_IP = args.wetter_intent_ip
WETTER_INTENT_SERVICE_PORT = args.wetter_intent_port

WIKIPEDIA_INTENT_SERVICE_IP = args.wikipedia_intent_ip
WIKIPEDIA_INTENT_SERVICE_PORT = args.wikipedia_intent_port

STUDIENORDNUNG_INTENT_SERVICE_IP = args.studienordnung_intent_ip
STUDIENORDNUNG_INTENT_SERVICE_PORT = args.studienordnung_intent_port

TODOLIST_INTENT_SERVICE_IP = args.todolist_intent_ip
TODOLIST_INTENT_SERVICE_PORT = args.todolist_intent_port

SEARCH_ENGINE_INTENT_SERVICE_IP = args.search_engine_intent_ip
SEARCH_ENGINE_INTENT_SERVICE_PORT = args.search_engine_intent_port

YOUTUBE_INTENT_SERVICE_IP = args.youtube_intent_ip
YOUTUBE_INTENT_SERVICE_PORT = args.youtube_intent_port
#############################################################################

ZEIT_STANDORT = "de_DE.UTF-8"
AUDIO_SAMPLE_RATE = 16000

ABSICHT_ABFRAGEN = 1
ABSICHT_EINGEBEN = 2
ABSICHT_ENTFERNEN = 3
ABSICHT_ZURUECKGEHEN = 4
ABSICHT_WEITERGEHEN = 5
ABSICHT_WIEDERHOLEN = 6
ABSICHT_ABBRECHEN = 7

SZENARIO_WETTER = 1
SZENARIO_STUDIENORDNUNG = 2
SZENARIO_WIKIPEDIA = 3
SZENARIO_TODO_LIST = 4
SZENARIO_UHRZEIT = 5
SZENARIO_DATUM = 6
SZENARIO_SYSTEM = 7
SZENARIO_YOUTUBE = 8
SZENARIO_SEARCH_ENGINE = 9

# ANMERKUNG_NONE = 1
ANMERKUNG_THEMA = 2
ANMERKUNG_AKTIVITAET = 3
ANMERKUNG_ZEIT = 4
ANMERKUNG_DATUM = 5
ANMERKUNG_ORT = 6

ERROR_VARIABLE_DATUM = 1
ERROR_VARIABLE_ZEIT = 2
ERROR_VARIABLE_ORT = 3
ERROR_VARIABLE_AKTIVITAET = 4
ERROR_VARIABLE_THEMA = 5
#############################################################################