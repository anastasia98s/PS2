# Datensatz-Szenarien und Absichten

#### **List-Szenario**
- **Anmerkungen**: Item
- **Absichten**: löschen, eingeben

#### Terminplan-Szenario
- **Anmerkungen**: Datum, Uhrzeit, Aufgabe
- **Absichten**: löschen, eingeben

#### Termin-Szenario
- **Anmerkungen**: Datum, Uhrzeit, Aufgabe, Ort
- **Absichten**: buchen, stornieren

#### Licht-Szenario
- **Anmerkungen**: Ort
- **Absichten**: dimmen, heller machen, ausschalten, einschalten

#### Kamera-Szenario
- **Anmerkungen**: Ort
- **Absichten**: zoom verringern, zoom vergrößern, ausschalten, einschalten, fotografieren, video aufnehmen

#### Musik-Szenario
- **Anmerkungen**: Musik, Person
- **Absichten**: abspielen, stoppen, ändern

#### Filme-Szenario
- **Anmerkungen**: Film (Name)
- **Absichten**: abspielen, stoppen

#### Video-Szenario
- **Anmerkungen**: URL
- **Absichten**: abspielen, stoppen

#### URL-Szenario
- **Anmerkungen**: URL
- **Absichten**: öffnen, indizieren

#### Nachricht-Szenario
- **Anmerkungen**: Telefonnummer, Nachricht
- **Absichten**: senden

#### Telefon-Szenario
- **Anmerkungen**: Telefonnummer
- **Absichten**: anrufen

#### Wetter-Szenario
- **Anmerkungen**: Datum, Uhrzeit, Ort
- **Absichten**: abfragen

#### Nachrichten-Szenario
- **Anmerkungen**: Datum, Kategorie
- **Absichten**: abfragen

#### Aktien-Szenario
- **Anmerkungen**: Aktie
- **Absichten**: verkaufen, abfragen, kaufen

#### Transport-Szenario
- **Anmerkungen**: Transport (Name, z.B. Taxi)
- **Absichten**: buchen, stornieren

#### Alarm-Szenario
- **Anmerkungen**: Datum, Uhrzeit
- **Absichten**: einstellen, entfernen/stoppen

#### Audio-Szenario
- **Anmerkungen**: Lautstärke (Zahl)
- **Absichten**: einstellen, verringern, erhöhen

#### Wikipedia-Szenario
- **Anmerkungen**: (??)
- **Absichten**: abfragen

#### Daten-Szenario
- **Anmerkungen**: Pfad, Datei (z.B. main.py)
- **Absichten**: drucken, lesen, öffnen, löschen, konvertieren

#### WLAN-Szenario
- **Anmerkungen**: Netzwerk (WLAN-Name)
- **Absichten**: verbinden, entfernen

#### Bluetooth-Szenario
- **Anmerkungen**: Gerät (Gerätename)
- **Absichten**: verbinden, entfernen

#### Berechnung-Szenario
- **Anmerkungen**: Zahl, Operator
- **Absichten**: berechnen

#### Timer-Szenario
- **Anmerkungen**: Uhrzeit
- **Absichten**: einstellen

#### Alarm-Szenario
- **Anmerkungen**: Datum, Uhrzeit
- **Absichten**: einstellen

#### System-Szenario
- **Anmerkungen**: -
- **Absichten**: stoppen, pausieren, fortsetzen, wiederholen

### Python-Klasse: Szenario (Intent)

Die folgende Python-Klasse implementiert das Szenario "List":

```python
class List:
    def __init__(self):
        self.items = []

    def löschen(self, Item):
        print(f"{Item} wurde aus der Liste entfernt")

    def eingeben(self, Item):
        print(f"{Item} wurde zur Liste hinzugefügt.")