## Erledigte Aufgaben

- Benutzer-Authentifizierung implementiert
- Textklassifizierung abgeschlossen
- Intentverteilung erstellt
- Sprach-zu-Text-Funktionalität integriert
- Text-zu-Sprach-Funktionalität implementiert
- Datenbank für Benutzer erstellt
- Intents "To-Do-Liste, Datum, Wetter, Uhrzeit" abgeschlossen

## ToDo
- Datenaufbereitung für Intents "Studienordnung, Wikipedia" im [Intends Ordner](intends).
- Mehr Datasets für Benutzer-Authentifizierung (Stimme) sammeln (für KI-Training).
- Mehr Datasets für Textklassifizierung sammeln (für KI-Training).

## Startanweisungen

1. **Installiere alle erforderlichen Pakete:**
   ```bash
   pip install -r requirements.txt
   ```

   **Hinweis:** Wenn es zu Fehlermeldungen kommt, kannst du die Pakete manuell installieren.

2. **Starte das Engine-Skript:**
   ```bash
   python engine.py
   ```

## To-Do-List Befehle
- **Was habe ich heute?**
- **Wann ist mein Meeting heute?**
- **Trage ein Meeting für morgen am Nachmittag ein.**
- **Trage ein Meeting heute um 12 Uhr ein.**
- **Füge ein Meeting am 18. Oktober hinzu.**
- **Kannst du mein Meeting morgen um 12 Uhr löschen?**
- **Kannst du mein heutes Meeting entfernen?**
- **Lösche mein Meeting.**

## Wetter-Befehle
- **Wie ist das Wetter heute?**
- **Wie wird das Wetter übermorgen?**
- **Zeig mir das Wetter für heute Abend.**
- **Wie wird das Wetter in Berlin?**

## Datum-Befehle
- **Welches Datum haben wir heute?**
- **Welches Datum war gestern?**
- **Was ist das Datum übermorgen?**

## Uhrzeit-Befehle
- **Wie spät ist es jetzt?**
- **Wie viel Uhr ist es?**
- **Wie viel Uhr ist es in Berlin?**
- **Welche Uhrzeit haben wir in New York?**

**Hinweis:** Um ein besseres Modell zu erhalten, kannst du im **Data-Controller** in `main.py` weitere Datensätze eingeben und trainieren.