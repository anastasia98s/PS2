## Erledigte Aufgaben
- Benutzer-Authentifizierung (Fingerabdruck einer Stimme) implementiert
- Textklassifizierung abgeschlossen
- Intentverteilung erstellt
- Sprach-zu-Text-Funktionalität integriert
- Text-zu-Sprach-Funktionalität implementiert
- Wake-Word-Funktionalität implementiert
- Datenbank erstellt
   - [Datenbank für Textklassifizierung (hauptsächlich für Datensatzeditoren)](data/data_controller/model_textklassifizierung.py)
   - [Datenbank für User + To-Do-Liste + Authentifizierung](data/data_controller/model_user.py)
- Intents "To-Do-Liste, Datum, Wetter, Uhrzeit" abgeschlossen
- Datasets/Testdaten zur Benutzerauthentifizierung (wird bei Verwendung automatisch gespeichert)

## To-Do
- Multithreading
- Mikroservice + API + neue Datenbank?
- Intents "Suchintend?, Studienordnung, Wikipedia" im [Intends Ordner](intends).
- Mehr Datasets/Testdaten für Textklassifizierung sammeln (für KI-Training).

## Startanweisungen
1. **Repository klonen und virtuelle Umgebung einrichten**
   ```shell
   git clone -b Nathaniel https://github.com/anastasia98s/PS2.git assistant_ai
   ```
   ```shell
   cd assistant_ai
   ```
   ```shell
   python -m venv ai_env
   ```
   ```shell
   ai_env\Scripts\activate
   ```
2. **Installiere alle erforderlichen Pakete:**
   ```shell
   pip install -r requirements.txt
   ```
   ```shell
   pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu124
   ```

   **Hinweis:**
   - Wenn es zu Fehlermeldungen kommt, kannst du die Pakete manuell installieren.
   - Wenn du das **trainierte Modell** benutzen willst, [Link zum Herunterladen](https://drive.google.com/file/d/1hehycFUbHL62oWO_ha_xQMGmWTobcfXx/view?usp=drive_link), dann musst du das `data`-Verzeichnis mit diesen Daten ersetzen.
   - Stelle sicher, dass FFMPEG installiert ist und im PATH-Umgebungsvariable eingetragen ist. [Link zum Herunterladen](https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip)

   ```shell
   ffmpeg -version
   ```
3. **Starte das Engine-Skript:**
   ```shell
   python engine.py
   ```

## To-Do-List Befehle
- **Hey Molly, Trage ein Meeting für morgen am Nachmittag ein!**
- **Hey Molly, Trage ein Meeting am Freitag um 12 Uhr ein!**
- **Hey Molly, Füge ein Jogging heute hinzu!**
- **Hey Molly, Setze einen Arzttermin am Freitag in To-Do-Liste!**
- **Hey Molly, Was habe ich heute?**
- **Molly, Was habe ich am Freitag?**
- **Molly, Wann ist mein Meeting am morgen?**
- **Molly, Kannst du mein Meeting morgen um 12 Uhr löschen?**
- **Molly, Kannst du mein heutes Meeting entfernen?**
- **Molly, lösche mein Meetting für Freitag!**

## Wetter-Befehle
- **Hey Molly, Wie ist das Wetter heute?**
- **Hey Molly, Wie ist das Wetter am Dienstag?**
- **Hey Molly, Wie wird das Wetter übermorgen?**
- **Molly, Zeig mir das Wetter für heute Abend.**
- **Molly, Wie wird das Wetter in Berlin?**

## Datum-Befehle
- **Hey Molly, Welches Datum haben wir heute?**
- **Hey Molly, Welches Datum war gestern?**
- **Molly, Was ist das Datum übermorgen?**
- **Molly, Welches Datum hat der Donnerstag?**

## Uhrzeit-Befehle
- **Hey Molly, Wie spät ist es jetzt?**
- **Hey Molly, Wie viel Uhr ist es?**
- **Molly, Wie viel Uhr ist es in Berlin?**
- **Molly, Welche Uhrzeit haben wir in New York?**

**Hinweis:** Um ein besseres Modell zu erhalten, kannst du im **Data-Controller** in `main.py` weitere Datensätze eingeben und trainieren.