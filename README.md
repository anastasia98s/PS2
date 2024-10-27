## Erledigte Aufgaben

- Benutzer-Authentifizierung implementiert
- Textklassifizierung abgeschlossen
- Intentverteilung erstellt
- Sprach-zu-Text-Funktionalität integriert
- Text-zu-Sprach-Funktionalität implementiert

## ToDo
- Datenbank für Benutzer und To-Do-Liste erstellen.
- Datenaufbereitung für Intents im [Intends Ordner](intends).
- Mehr Datasets für Benutzer-Authentifizierung (Stimme) sammeln (für KI-Training).
- Mehr Datasets für Textklassifizierung sammeln (für KI-Training).

## Startanweisungen

1. **Installiere alle erforderlichen Pakete:**
   ```bash
   pip install -r requirements.txt
   ```

   **Hinweis:** Wenn es zu Fehlermeldungen kommt, kannst du die Pakete manuell installieren.

2. **Starte das Hauptskript:**
   ```bash
   python main.py
   ```

3. **Trainiere die Modelle:**
   - Textklassifizierung - und Authentifizierung KI mindestens 1x trainieren.
   
   ### Textklassifizierung KI (im main.py)
   1. Menu 1 wählen: **Option 1**.
   2. Menu 2 wählen: **Option 2**.

   ### Authentifizierung KI (im main.py)
   1. Menu wählen: **Option 2**.
   2. Menu wählen: **Option 2**.

4. **Starte das Engine-Skript:**
   ```bash
   python engine.py
   ```

# Datensatz-Szenarien und Absichten

#### **ToDo-List-Szenario**
- **Anmerkungen**: Artikel, List, Zustand, UserID
- **Absichten**: eingeben, löschen, ändern, abfragen

#### **Datum-Szenario**
- **Anmerkungen**: Datum
- **Absichten**: abfragen

#### **Studienordnung-Szenario**
- **Anmerkungen**: Thema
- **Absichten**: abfragen

#### **Wetter-Szenario**
- **Anmerkungen**: Datum, Zeit, Ort
- **Absichten**: abfragen

#### **Wikipedia-Szenario**
- **Anmerkungen**: Thema
- **Absichten**: abfragen

#### **Zeit-Szenario**
- **Anmerkungen**: Ort
- **Absichten**: abfragen