# Architektur für das Assistant AI Projekt

## 1. **Benutzerdatenbank Struktur**
![Benutzerdatenbank](docs_image/benutzerprofil.png)
- **Hauptinhalt**: Benutzerdaten, Merkmale, TODO
- **Merkmale**: Datensatz zur Trainings-Authentifikations-KI
![Beispielinhalt der Benutzerdatenbank](docs_image/ex_data_benutzer_db.png)

## 2. **Textklassifizierungsdatenbank Struktur**
![Textklassifizierungsdatenbank](docs_image/textklassifizierung.png)
- **Hauptinhalt**: Sätze, Anmerkungen, Szenarien, Absichten
![Beispielinhalt der Textklassifizierungsdatenbank](docs_image/ex_data_textklassifizierung_db.png)

## 3. **KI-Technologie**
- **Intent- und Entitätserkennung (BERT Architektur)**: Modell zur Erkennung von Benutzereingaben und Entitäten wie Zeit, Ort und Aktivität.
- **Authentifizierung der Benutzer (CNN Modell)**: Identifiziert Benutzer durch Stimme.
- **Spracherkennungsmodell (Whisper)**: Transkribiert gesprochene Sprache.
- **Text-zu-Sprache-Modell (Microsoft)**: Generiert gesprochene Antworten aus Text.

## 4. **Benutzerschnittstellen**
- **Datensatz-Editor**: Ermöglicht das Bearbeiten von Textklassifizierungs-Datensätzen.

## 5. **Datenflussdiagramm**
![Datenflussdiagramm](docs_image/einfaches_diagramm.drawio.png)

## 6. **Authentifizierung/Anmeldung Aktivitätsdiagramm**
![Aktivitätsdiagramm](docs_image/user_anmeldung.drawio.png)