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
   ```shell
   python main.py --ip [Shared-Data-Service-IP] --port [Shared-Data-Service-Port]
   ```
   **Hinweis:**
   - Es gibt 13 Microservice.
   - Der erste Microservice, der gestartet werden muss, ist der Shared-Data-Service.
   - Der zweite Microservice, der gestartet werden muss, ist der Kontoverwaltung-Service.