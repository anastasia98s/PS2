@echo off
cd /d "%~dp0\system\shared_data"
start python main.py --ip localhost --port 8000
timeout /t 5 /nobreak > nul

cd /d "%~dp0\system\kontoverwaltung"
start python main.py --ip localhost --port 8000

cd /d "%~dp0\system\speech_to_text"
start python main.py --ip localhost --port 8000

cd /d "%~dp0\system\text_to_speech"
start python main.py --ip localhost --port 8000

cd /d "%~dp0\system\textklassifizierung"
start python main.py --ip localhost --port 8000

cd /d "%~dp0\intents\datum"
start python main.py --ip localhost --port 8000

cd /d "%~dp0\intents\search_engine"
start python main.py --ip localhost --port 8000

cd /d "%~dp0\intents\studienordnung"
start python main.py --ip localhost --port 8000

cd /d "%~dp0\intents\todolist"
start python main.py --ip localhost --port 8000

cd /d "%~dp0\intents\uhrzeit"
start python main.py --ip localhost --port 8000

cd /d "%~dp0\intents\wetter"
start python main.py --ip localhost --port 8000

cd /d "%~dp0\intents\wikipedia"
start python main.py --ip localhost --port 8000

cd /d "%~dp0\intents\youtube"
start python main.py --ip localhost --port 8000