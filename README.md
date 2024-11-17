## Erledigte Aufgaben
- Textklassifizierung abgeschlossen
- Textklassifizierung mit Intents verbunden
- Speech-zu-Text-Funktionalität implementiert
- Text-zu-Speech-Funktionalität implementiert
- Multithreading für ASR implementiert
- Datenbank erstellt
   - [Datenbank für Textklassifizierung (hauptsächlich für Datensatzeditoren)](data/data_controller/model_textklassifizierung.py)
   - [Datenbank für User + To-Do-Liste + Authentifizierung](data/data_controller/model_user.py)
- Intents "To-Do-Liste, Studienordnung, Datum, Wetter, Uhrzeit" abgeschlossen
- Benutzer-Authentifizierung implementiert. *(Fingerabdruck einer Stimme)*
- automatische Datasets/Testdaten zur Benutzerauthentifizierung implementiert. *(wird bei Verwendung automatisch gespeichert)*
- Aktivierungswort-Funktionalität implementiert. *(Du musst den Aktivierungswort-Rufnamen-Assistenten in der Datei main.py mit deiner eigenen Stimme aufnehmen und trainieren)*
- **trainierte Modell** auf der Cloud hochgeladen. [Link zum Herunterladen](https://drive.google.com/drive/folders/1I27FN5USWLdT6kTXWMWGypINOeeF8oru?usp=drive_link)
   - *musst du nur das `data`-Verzeichnis durch diese Daten richtig ersetzen.*

## To-Do
- Multithreading/Multiprocessing implementieren
- Mikroservice + API + neue Datenbank? erstellen
- Intents "Suchintent, Wikipedia" erstellen. [Intends Ordner](intents).
- Mehr Datasets/Testdaten für Textklassifizierung sammeln. *(weitere Datensätze in den **Data-Controller** in `main.py` eingeben)*

## Architektur
Um mehr über die Architektur des Projekts zu erfahren, siehe die [Architektur-Dokumentation](docs/ARCHITEKTUR.md).

## Startanweisungen (9 GB + Ollama Speicherplatz erforderlich)
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
   - Stelle sicher, dass Ollama installiert ist. Weitere Informationen und den Download findest du hier: [Link zum Herunterladen](https://ollama.com/download/windows).
   - Überprüfe, ob das LLM-Modell von Ollama bereits heruntergeladen wurde. *(den LLM-Modellnamen findest du in `config.py`)*

   ```shell
   ffmpeg -version
   ```
   ```shell
   ollama -v
   ```
4. **Aktivierungswort mit eigener Stimme aufnehmen und trainieren:**
   1. Öffne `main.py`.
   2. Suche das Menü „Aktivierungswort aufnehmen“.
   3. Sprich die folgenden Beispiele nach:
      - **Aktivierungswort:**
         - Hey [Name]
         - [Name]
         - … (Wiederhole so viele Varianten wie möglich)
      - **Kein Aktivierungswort:**
         - [Zufällige Rede]
         - [Zufällige Geräusche]
   4. Wenn du fertig bist, trainiere die Datensätze.
5. **Starte das Engine-Skript:**
   ```shell
   python engine.py
   ```

   **Hinweis:**
   - Wenn du das **trainierte Modell** benutzen willst, [Link zum Herunterladen](https://drive.google.com/drive/folders/1I27FN5USWLdT6kTXWMWGypINOeeF8oru?usp=drive_link), dann musst du das `data`-Verzeichnis durch diese Daten richtig ersetzen.

## Assistenten aufrufen
- Du musst zunächst den Assistenten aktivieren, indem du das Aktivierungswort verwendest.
1. **Benutzer**: Hey [Name]
2. **Assistent**: Ja
3. **Benutzer**: `Befehl eingeben`

## To-Do-List Befehle
- **Eingeben**
   - Trage ein Meeting für morgen Nachmittag ein!
   - Trage ein Meeting am Freitag um 12 Uhr ein!
   - Füge ein Jogging heute Abend hinzu!
   - Setze einen Arzttermin am Freitag um 13 Uhr in die To-Do-Liste!

- **Abfragen**
   - **Zeit abfragen**
      - Wann ist mein Meeting?
   - **Aktivität zu einem bestimmten Zeitpunkt abfragen**
      - Was habe ich am 12. Oktober um 12 Uhr?
      - Was habe ich heute Nachmittag?
      - Wann ist mein Meeting morgen früh?
      - Was habe ich um 12:30 Uhr am Freitag?
   - **Aktivität an einem bestimmten Datum abfragen**
      - Was habe ich heute?
      - Was hatte ich (vor)gestern?
      - Was habe ich am Freitag?
      - Was habe ich am 02. Dezember 2025?

- **Löschen**
   - **Alle genannten Aktivitäten löschen**
      - Löscht mein Meeting!
   - **Alle genannten Aktivitäten an einem Tag löschen**
      - Kannst du mein heutiges Meeting entfernen?
      - Lösche mein Meeting für Freitag!
   - **Bestimmte Aktivität löschen**
      - Kannst du mein Meeting morgen um 12:10 Uhr löschen?

## Wetter-Befehle
- **Wetter zu einem Zeitpunkt**
   - Wie ist das Wetter am 11.12. um 12 Uhr?
   - Wie ist das Wetter morgen früh?

- **Wetter an einem Datum**
   - Wie ist das Wetter am Dienstag?
   - Wie ist das Wetter heute?
   - Wie wird das Wetter übermorgen?
   - Wie ist das Wetter am 11.10?
   - Wie ist das Wetter?

- **Wetter an einem Ort**
   - Wie wird das Wetter morgen um 12:30 in Rio de Janeiro?
   - Zeig mir das Wetter für heute Abend in New York.
   - Wie wird das Wetter in Berlin?

## Datum-Befehle
- Welches Datum haben wir heute?
- Welches Datum war (vor)gestern?
- Was ist das Datum übermorgen?
- Welches Datum hat der Donnerstag?

## Uhrzeit-Befehle
- Wie spät ist es jetzt?
- Wie viel Uhr ist es in Berlin?
- Welche Uhrzeit haben wir in New York?

## Studienordnung Befehle
- Was ist eine PVL?
- Wie läuft ne Mündliche Prüfung ab?
- Was ist ein Freiversuch?
- Wie lange geht das Praktikum?
- Wann bekomme ich eine 2?
- Was passiert, wenn ich mehrfach um eine Prüfung falle?
- Wie kann ich meine Prüfung einsehen?
- Kann ich mir Module von einem anderen Studiengang anrechnen lassen?
- Wie wird das Praktikum bewertet?
- Wer darf eine Bachelorarbeit betreuen?
- Was ist ein Beleg?
- Wie kann ich mich von einer Prüfung abmelden?
- [mehr](https://github.com/anastasia98s/PS2/blob/PDF_Intent/testdaten.txt)

## Wikipedia Befehle
- TODO

## Suchintent Befehle
- TODO

**Hinweis:** Um ein besseres Modell zu erhalten, kannst du im **Data-Controller** in `main.py` weitere Datensätze eingeben und trainieren.