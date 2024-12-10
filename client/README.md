## Startanweisungen
1. **Repository klonen und virtuelle Umgebung einrichten**
   ```shell
   git clone -b Nathaniel https://github.com/anastasia98s/PS2.git assistant_ai
   ```
   ```shell
   cd assistant_ai\client
   ```
   ```shell
   python -m venv assistant_ai_client
   ```
   ```shell
   assistant_ai_client\Scripts\activate
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
   - **Trainierte Modelle** auf der Cloud. [Link zum Herunterladen](https://drive.google.com/drive/folders/1I27FN5USWLdT6kTXWMWGypINOeeF8oru?usp=drive_link)

1. **Aktivierungswort mit eigener Stimme aufnehmen und trainieren:**
   1. Öffne `setting.py`.
      ```shell
      python setting.py --ip [Server-Shared-Data-Service-IP] --port [Server-Shared-Data-Service-PORT]
      ```
   2. Suche das Menü „Aktivierungswort aufnehmen“.
   3. Sprich die folgenden Beispiele nach:
      - **Aktivierungswort:**
         - Hey [Name]
         - [Name]
         - … (Wiederhole 20-30 Mal)
      - **Kein Aktivierungswort:**
         - [Zufällige Rede]
         - [Zufällige Geräusche]
         - … (Wiederhole 20-30 Mal)
   4. Wenn du fertig bist, trainiere die Datensätze.

   **Hinweis:**
   - **HTW DRESDEN SERVER** 
      - Server-Shared-Data-Service-IP: `141.56.137.185`
      - Server-Shared-Data-Service-Port: `8000`

2. **Starte das Engine-Skript:**
   ```shell
   python engine.py --ip [Server-Shared-Data-Service-IP] --port [Server-Shared-Data-Service-PORT]
   ```

   **Hinweis:**
   - **HTW DRESDEN SERVER** 
      - Server-Shared-Data-Service-IP: `141.56.137.185`
      - Server-Shared-Data-Service-Port: `8000`

## Assistenten aufrufen
- Du musst zunächst den Assistenten aktivieren, indem du das Aktivierungswort verwendest.
1. **Benutzer**: Hey [Name]
2. **Assistent**: Ja
3. **Benutzer**: `Befehl eingeben`