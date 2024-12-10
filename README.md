## Erledigte Aufgaben
- Textklassifizierung abgeschlossen
- Textklassifizierung mit Intents verbunden
- Speech-zu-Text-Funktionalität implementiert
- Text-zu-Speech-Funktionalität implementiert
- Multithreading implementiert
- Confusion Matrix implementiert
- Mikroservice implementiert
- Datenbank erstellt
- Intents "To-Do-Liste, Studienordnung, Datum, Wetter, Uhrzeit, Suchintent, Wikipedia" abgeschlossen
- Benutzer-Authentifizierung implementiert. *(Fingerabdruck einer Stimme)*
- automatische Datasets/Testdaten zur Benutzerauthentifizierung implementiert. *(wird bei Verwendung automatisch gespeichert)*
- Aktivierungswort-Funktionalität implementiert.

## Architektur
Um mehr über die Architektur des Projekts zu erfahren, siehe die [Architektur-Dokumentation](docs/ARCHITEKTUR.md).

## Test
[Test-Dokumentation](docs/TEST.md).

# Testdaten
## To-Do-List
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

## Datum
- Welches Datum haben wir heute?
- Welches Datum war (vor)gestern?
- Was ist das Datum übermorgen?
- Welches Datum hat der Donnerstag?

## Uhrzeit
- Wie spät ist es jetzt?
- Wie viel Uhr ist es in Berlin?
- Welche Uhrzeit haben wir in New York?

## Studienordnung
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

## Wikipedia
- Wer ist Barack Obama?
- Was ist Deutschland?
- Informationen zu Dresden
- Was ist eine Lerche?
- Was sind Pommes?
- Was ist ein Auto?
- Wer war Angela Merkel?
- Was ist der Eiffelturm?
- Was ist ein Flugzeug?
- Was ist der Mount Everest?
- Was ist der Amazonas?
- Wer war Albert Einstein?
- Was ist die Berliner Mauer?
- Gib mir mehr Informationen über Nanotechnologie
- Wer war Ludwig van Beethoven?
- Was fällt unter den Begriff Ethik
- Was bedeutet Python?
- Definiere maschinelles Lernen.
- Erkläre was ein Algorithmus ist.
- Erkläre den Begriff Quantenphysik?
- Gib mir die Definition von Künstliche Intelligenz?
- Was versteht man unter Demokratie?
- Was ist der Begriff Nachhaltigkeit?
- Was ist damit gemeint, wenn von Cybersecurity gesprochen wird?
- [mehr](https://github.com/anastasia98s/PS2/blob/Wikipedia-Intent/testdaten_2.txt)

## Suchintent Wetter
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

## Suchintent Youtube
- **Youtube abspielen**
   - Such nach dem Podcast über Künstliche Intelligenz auf YouTube
   - Finde den Podcast von Fest und Flauschig auf YouTube
   - Such nach Musik von Beethoven auf YouTube
   - Spiel Let It Be von The Beatles auf YouTube
   - Such nach Shape of You auf YouTube
   - Finde ein Video über gesunde Ernährung
   - Such nach einem Video über Tipps für bessere Fotografie
   - Spiel ein Video über AI ab
- **Youtube herunterladen (als Audio)**
   - Lade das neueste Video von PewDiePie herunter
   - Lade ein lustiges Video herunter
   - Lade dieses Video herunter

## Suchintent Search Engine
- Such nach einem Hotel in Berlin
- Finde eine Ferienwohnung in München
- Such nach einem Kinoticket für den Film Avatar 2
- Finde Tickets für das Theaterstück Hamlet
- Flugticket nach Berlin
- Zugticket nach München
- Heutige Nachrichten zum Klimawandel
- Nachrichten heute über die Corona-Pandemie
- Beste Aktien 2024
- Dividendenaktien
- Aktienmarkt Nachrichten
- Rezept Spaghetti Bolognese
- Vegane Lasagne Rezept
- Finde ein Rezept für indisches Curry
- Such nach einem Rezept für Pfannkuchen

## System Befehle (für Intent)
- Gehe zurück
- Weiter
- Gehe weiter
- Beende das
- Gehe zur vorherigen Musik
- Schließe die Website
- Abbrechen das Video
- Beende die Wiedergabe des Musikstücks
- Starten Sie die Website neu
- Gehe zum vorherigen Video
- Weiter mit dem nächsten Video
- Lade das nächste Video