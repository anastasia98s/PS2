# Architektur für das Assistant AI Projekt

## 1. **Benutzerdatenbank Struktur**
![Benutzerdatenbank](docs_image/benutzerprofil.png)
- **Hauptinhalt**: Benutzerdaten, Merkmale, TODO
- **Merkmale**: Datensatz zur Trainings-Authentifikations-KI

![Beispielinhalt der Benutzerdatenbank](docs_image/ex_data_benutzer_db.png)

## 2. **Aktivierungswort-Datenbank Struktur**
![Textklassifizierungsdatenbank](docs_image/textklassifizierung.png)
- **Hauptinhalt**: Sätze, Anmerkungen, Szenarien, Absichten

![Beispielinhalt der Textklassifizierungsdatenbank](docs_image/ex_data_textklassifizierung_db.png)

## 3. **Aktivierungswort-Datenbank Struktur**
![Aktivierungswort-Datenbank](docs_image/aktivierungswort.png)

![Beispielinhalt der Aktivierungswort-Datenbank](docs_image/ex_data_aktivierungswort_db.png)

## 4. **KI-Technologie**
- **Intent- und Entitätserkennung (BERT Architektur)**: erkennt Benutzereingaben und Entitäten
- **Authentifizierung der Benutzer (CNN-Modell)**: identifiziert Benutzer durch ihre Stimme
- **Aktivierungswort (CNN-Modell)**: identifiziert den Aufruf des Benutzers an den Assistenten
- **Spracherkennungsmodell (Whisper)**: transkribiert gesprochene Sprache in Text
- **Text-zu-Sprache-Modell (Microsoft)**: generiert gesprochene Antworten aus Text
- **PDF-Verstehen (Ollama)**: beantwortet Fragen zu Inhalten eines PDFs

![KI-Modell](docs_image/KI-Modell.drawio.png)

## 5. **Datenflussdiagramm**
![Datenflussdiagramm](docs_image/komplexes_diagramm.drawio.png)

<!-- - **einfaches Version**

![Einfaches Datenflussdiagramm](docs_image/einfaches_diagramm.drawio.png) -->

## 6. **Authentifizierung/Anmeldung Aktivitätsdiagramm**
![Aktivitätsdiagramm](docs_image/user_anmeldung.drawio.png)

## 7. **Confusion Matrix**
### Confusion Matrix von Authentifizierung-KI

![Confusion Matrix von Authentifizierung-KI](docs_image/auth_matrix.png)

### Confusion Matrix von Aktivierungswort-KI

![Confusion Matrix von Aktivierungswort-KI](docs_image/aktivierung_cm.png)

### Confusion Matrix von Textklassifizierung-KI (Anmerkung)

![Confusion Matrix von Textklassifizierung-KI (Anmerkung)](docs_image/anmerkung_cm.png)

### Confusion Matrix von Textklassifizierung-KI (Absicht)

![Confusion Matrix von Textklassifizierung-KI (Absicht)](docs_image/absicht_cm.png)

### Confusion Matrix von Textklassifizierung-KI (Szenario)

![Confusion Matrix von Textklassifizierung-KI (Szenario)](docs_image/szenario_cm.png)


# Intents-Sturktur

Die Textklassifikation KI gibt einen Output in drei Hauptkategorien zurück:

1. **Szenario**: Dies ist der Klassenname, der das Kontextumfeld der Anfrage beschreibt.
2. **Absicht**: Dies ist die Funktion innerhalb der jeweiligen Klasse (Szenario).
3. **Anmerkung**: Dies sind die Variablen, die für die Absicht innerhalb des Szenarios verwendet werden.

## Beispiel:
- Wie ist das Wetter heute in Berlin
  - **Szenario**: "Wetter"
  - **Absicht**: "abfragen"
  - **Anmerkung**: "Standort: Berlin", "Datum: heute"

- Lösche meine Besprechung morgen um 12 Uhr
  - **Szenario**: "Todo-Liste"
  - **Absicht**: "löschen"
  - **Anmerkung**: "Aktivität: Besprechung", "Datum: morgen", "Uhrzeit: 12 Uhr"