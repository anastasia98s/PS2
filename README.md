## Erledigte Aufgaben

- Benutzer-Authentifizierung implementiert
- Textklassifizierung abgeschlossen
- Intentverteilung erstellt
- Sprach-zu-Text-Funktionalität integriert
- Text-zu-Sprach-Funktionalität implementiert
- Datenbank erstellt
   - [Datenbank für Textklassifizierung (hauptsächlich für Datensatzeditoren)](data/data_controller/model_textklassifizierung.py)
   - [Datenbank für User + To-Do-Liste + Authentifizierung](data/data_controller/model_user.py)
- Intents "To-Do-Liste, Datum, Wetter, Uhrzeit" abgeschlossen

## ToDo
- Datenaufbereitung für Intents "Studienordnung, Wikipedia" im [Intends Ordner](intends).
- Mehr Datasets für Benutzer-Authentifizierung (Stimme) sammeln (für KI-Training).
- Mehr Datasets für Textklassifizierung sammeln (für KI-Training).

## Startanweisungen
1. **Repository klonen und virtuelle Umgebung einrichten**
   ```bash
   git clone -b Nathaniel https://github.com/anastasia98s/PS2.git assistant_ai
   cd assistant_ai
   python -m venv ai_env
   ai_env\Scripts\activate
   ```
2. **Installiere alle erforderlichen Pakete:**
   ```bash
   pip install -r requirements.txt
   pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu124
   ```

   **Hinweis:**
   - Wenn es zu Fehlermeldungen kommt, kannst du die Pakete manuell installieren.
   - Wenn du das trainierte Modell benutzen will, [klicke hier](https://drive.google.com/file/d/1hehycFUbHL62oWO_ha_xQMGmWTobcfXx/view?usp=drive_link), dann musst du das `data`-Verzeichnis mit diesen Daten ersetzen.
   - Stelle sicher, dass FFMPEG installiert ist und im PATH-Umgebungsvariable eingetragen ist. [Link zum Herunterladen](https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip)

3. **Starte das Engine-Skript:**
   ```bash
   python engine.py
   ```

## To-Do-List Befehle
- **Trage ein Meeting für morgen am Nachmittag ein!**
- **Trage ein Meeting am Freitag um 12 Uhr ein!**
- **Füge ein Jogging heute hinzu!**
- **Setze einen Arzttermin am Freitag in To-Do-Liste!**
- **Was habe ich heute?**
- **Was habe ich am Freitag?**
- **Wann ist mein Meeting am morgen?**
- **Kannst du mein Meeting morgen um 12 Uhr löschen?**
- **Kannst du mein heutes Meeting entfernen?**
- **lösche mein Meetting für Freitag!**

## Wetter-Befehle
- **Wie ist das Wetter heute?**
- **Wie ist das Wetter am Dienstag?**
- **Wie wird das Wetter übermorgen?**
- **Zeig mir das Wetter für heute Abend.**
- **Wie wird das Wetter in Berlin?**

## Datum-Befehle
- **Welches Datum haben wir heute?**
- **Welches Datum war gestern?**
- **Was ist das Datum übermorgen?**
- **Welches Datum hat der Donnerstag?**

## Uhrzeit-Befehle
- **Wie spät ist es jetzt?**
- **Wie viel Uhr ist es?**
- **Wie viel Uhr ist es in Berlin?**
- **Welche Uhrzeit haben wir in New York?**

**Hinweis:** Um ein besseres Modell zu erhalten, kannst du im **Data-Controller** in `main.py` weitere Datensätze eingeben und trainieren.