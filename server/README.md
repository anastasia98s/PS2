## Startanweisungen
1. **Repository klonen und virtuelle Umgebung einrichten**
```shell
git clone -b Nathaniel https://github.com/anastasia98s/PS2.git assistant_ai
```
```shell
cd assistant_ai\server
```
```shell
python -m venv assistant_ai_server
```
```shell
assistant_ai_server\Scripts\activate
```
   
2. **Installiere alle erforderlichen Pakete:**
```shell
pip install -r requirements.txt
```
```shell
playwright install
```

- (Optional) Wenn du schneller mit der GPU arbeiten möchtest
   ```shell
   pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu124
   ```

**Hinweis:**
- Python 3.12 und höher ist für TTS nicht kompatibel. *(Python 3.11.4 ohne Probleme)*
- FFMPEG installieren und PATH-Umgebungsvariable eintragen: [Link zum Herunterladen](https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip)
- Ollama installieren: [Link zum Herunterladen](https://ollama.com/download/windows).
- LLM-Modell bei Ollama installieren. *(der LLM-Modellname: `llama3.2:latest`)*
- **trainierte Modelle** auf der Cloud. [Link zum Herunterladen](https://drive.google.com/drive/folders/1I27FN5USWLdT6kTXWMWGypINOeeF8oru?usp=drive_link)

```shell
ffmpeg -version
```
```shell
ollama -v
```

3. **Starte alle Microservices:**
**Main-Server-Service**
```shell
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
```
**Services (außer dem Main-Server)**
```shell
python main.py --main_server_ip localhost --main_server_port 8000
```
**Hinweis:**
- Es gibt 13 Microservice.
- Der erste Microservice, der gestartet werden muss, ist der Main-Server-Service.
- Der zweite Microservice, der gestartet werden muss, ist der Kontoverwaltung-Service.