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

   <!-- **Hinweis:**
   - **Trainierte Modelle** auf der Cloud. [Link zum Herunterladen](https://drive.google.com/drive/folders/1I27FN5USWLdT6kTXWMWGypINOeeF8oru?usp=drive_link) -->

<!-- 1. **Aktivierungswort mit eigener Stimme aufnehmen und trainieren:**
   1. Öffne `setting.py`.
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
      - Server-IP: `141.56.137.185`
      - Server-Port: `8000` -->

2. **Starte das Engine-Skript:**
   ```shell
   python engine.py
   ```

   **Hinweis:**
   - **HTW DRESDEN SERVER**
      - Server-IP: `141.56.137.185`
      - Server-Port: `8000`

## Assistenten aufrufen
**Standardaktivierungswort: `Tim`**
1. **Benutzer**: Hey Tim
2. **Assistent**: Ja
3. **Benutzer**: `Befehl eingeben`

**Hinweis**: Der Assistent verwendet standardmäßig den Windows Media Player, um Audio auszugeben. Falls der MediaPlayer jedoch nicht funktioniert, können Sie eine andere Audio-Wiedergabe-Software verwenden.