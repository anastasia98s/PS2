@echo off
python main.py ^
  --main_server_ip localhost --main_server_port 8000 ^
  --kontoverwaltung_ip localhost --kontoverwaltung_port 8001 ^
  --textklassifizierung_ip localhost --textklassifizierung_port 8002 ^
  --speech_to_text_ip localhost --speech_to_text_port 8003 ^
  --text_to_speech_ip localhost --text_to_speech_port 8004 ^
  --datum_intent_ip localhost --datum_intent_port 8005 ^
  --uhrzeit_intent_ip localhost --uhrzeit_intent_port 8006 ^
  --wetter_intent_ip localhost --wetter_intent_port 8007 ^
  --wikipedia_intent_ip localhost --wikipedia_intent_port 8008 ^
  --studienordnung_intent_ip localhost --studienordnung_intent_port 8009 ^
  --todolist_intent_ip localhost --todolist_intent_port 8010 ^
  --search_engine_intent_ip localhost --search_engine_intent_port 8011 ^
  --youtube_intent_ip localhost --youtube_intent_port 8012
pause