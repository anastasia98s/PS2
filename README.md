## Erledigte Aufgaben
- Textklassifizierung abgeschlossen
- Textklassifizierung mit Intents verbunden
- Speech-zu-Text-Funktionalität implementiert
- Text-zu-Speech-Funktionalität implementiert
- Datenbank erstellt
   - [Datenbank für Textklassifizierung (hauptsächlich für Datensatzeditoren)](data/data_controller/model_textklassifizierung.py)
   - [Datenbank für User + To-Do-Liste + Authentifizierung](data/data_controller/model_user.py)
- Intents "To-Do-Liste, Datum, Wetter, Uhrzeit" abgeschlossen
- Benutzer-Authentifizierung implementiert. *(Fingerabdruck einer Stimme)*
- automatische Datasets/Testdaten zur Benutzerauthentifizierung implementiert. *(wird bei Verwendung automatisch gespeichert)*
- Wake-Word-Funktionalität implementiert. *(Standard-Wake-Word: **Molly**. oder Wake-Word in `config.py` anpassen)*
- **trainierte Modell** auf der Cloud hochgeladen. [Link zum Herunterladen](https://drive.google.com/drive/folders/1I27FN5USWLdT6kTXWMWGypINOeeF8oru?usp=drive_link)
   - *musst du nur das `data`-Verzeichnis durch diese Daten richtig ersetzen.*

## To-Do
- Multithreading implementieren
- Mikroservice + API + neue Datenbank? erstellen
- Intents "Suchintent?, Studienordnung, Wikipedia" erstellen. [Intends Ordner](intends).
- Mehr Datasets/Testdaten für Textklassifizierung sammeln. *(weitere Datensätze in den **Data-Controller** in `main.py` eingeben)*

## Startanweisungen (9 GB Speicherplatz erforderlich)
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
   - Wenn es zu Fehlermeldungen kommt, kannst du die Pakete manuell installieren. *(Ich benutze Python 3.11.9 und 3.12.1 ohne Probleme)*
   - Stelle sicher, dass FFMPEG installiert ist und im PATH-Umgebungsvariable eingetragen ist. [Link zum Herunterladen](https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip)

   ```shell
   ffmpeg -version
   ```
3. **Starte das Engine-Skript:**
   ```shell
   python engine.py
   ```

   **Hinweis:**
   - Wenn du das **trainierte Modell** benutzen willst, [Link zum Herunterladen](https://drive.google.com/drive/folders/1I27FN5USWLdT6kTXWMWGypINOeeF8oru?usp=drive_link), dann musst du das `data`-Verzeichnis durch diese Daten richtig ersetzen.

## To-Do-List Befehle
- **Eingeben**
   - Hey Molly, trage ein Meeting für morgen Nachmittag ein!
   - Hey Molly, trage ein Meeting am Freitag um 12 Uhr ein!
   - Hey Molly, füge ein Jogging heute Abend hinzu!
   - Hey Molly, setze einen Arzttermin am Freitag um 13 Uhr in die To-Do-Liste!

- **Abfragen**
   - **Zeit abfragen**
      - Hey Molly, wann ist mein Meeting?
   - **Aktivität zu einem bestimmten Zeitpunkt abfragen**
      - Hey Molly, was habe ich am 12. Oktober/12. Oktober 2025/12.10 um 12 Uhr?
      - Hey Molly, was habe ich heute Nachmittag?
      - Wann ist mein Meeting morgen früh, Molly?
      - Hey Molly, was habe ich um 12:30 Uhr am Freitag?
   - **Aktivität an einem bestimmten Datum abfragen**
      - Hey Molly, was habe ich heute?
      - Hey Molly, was hatte ich (vor)gestern?
      - Was habe ich am Freitag, Molly?
      - Hey Molly, was habe ich am 02. Dezember?

- **Löschen**
   - **Alle genannten Aktivitäten löschen**
      - Hey Molly, kannst du mein Meeting morgen um 12 Uhr löschen?
   - **Alle genannten Aktivitäten an einem Tag löschen**
      - Molly, kannst du mein heutiges Meeting entfernen?
      - Molly, lösche mein Meeting für Freitag!
   - **Bestimmte Aktivität löschen**
      - Hey Molly, kannst du mein Meeting morgen um 12:10 Uhr löschen?

## Wetter-Befehle
- **Wetter zu einem Zeitpunkt**
   - Hey Molly, wie ist das Wetter um 12 Uhr am 11.12.?
   - Hey Molly, wie ist das Wetter morgen früh?

- **Wetter an einem Datum**
   - Hey Molly, wie ist das Wetter am Dienstag?
   - Hey Molly, wie ist das Wetter heute?
   - Wie wird das Wetter übermorgen, Molly?
   - Hey Molly, wie ist das Wetter?

- **Wetter an einem Ort**
   - Molly, wie wird das Wetter morgen um 12:30 in Rio de Janeiro?
   - Molly, zeig mir das Wetter für heute Abend in New York.
   - Molly, wie wird das Wetter in Berlin?

## Datum-Befehle
- Hey Molly, welches Datum haben wir heute?
- Hey Molly, welches Datum war (vor)gestern?
- Was ist das Datum übermorgen, Molly?
- Molly, welches Datum hat der Donnerstag?

## Uhrzeit-Befehle
- Hey Molly, wie spät ist es jetzt?
- Wie viel Uhr ist es in Berlin, Molly?
- Molly, welche Uhrzeit haben wir in New York?

## Studienordnung Befehle
- TODO

## Wikipedia Befehle
- TODO

## Suchintent Befehle
- TODO

**Hinweis:** Um ein besseres Modell zu erhalten, kannst du im **Data-Controller** in `main.py` weitere Datensätze eingeben und trainieren.