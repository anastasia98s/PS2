## Erledigte Aufgaben

- Benutzer-Authentifizierung implementiert
- Textklassifizierung abgeschlossen
- Intentverteilung erstellt
- Sprach-zu-Text-Funktionalität integriert
- Text-zu-Sprach-Funktionalität implementiert

## ToDo

- Datenaufbereitung für Intents im [Intends Ordner](Intends).
- Mehr Datasets für Benutzer-Authentifizierung sammeln
- Mehr Datasets für Textklassifizierung sammeln

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
   - AI Text und AI Authentifizierung mindestens 1x trainieren.

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