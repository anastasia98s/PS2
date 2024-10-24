# Datensatz-Szenarien und Absichten

#### **Alarm-Szenario**
- **Anmerkungen**: Datum, Zeit, Frequenz, Aktivität
- **Absichten**: einstellen, entfernen, abfragen

#### **Liste-Szenario**
- **Anmerkungen**: Artikel, Menge, Thema?
- **Absichten**: eingeben, löschen, ändern, abfragen

#### **Kalender-Szenario**
- **Anmerkungen**: Datum, Zeit, Ort, Aktivität
- **Absichten**: einstellen, ändern, löschen, eingeben, abfragen

#### **DateZeit-Szenario**
- **Anmerkungen**: Datum, Zeit, Zeitzone, Ort, Thema?
- **Absichten**: konvertieren, abfragen

#### **Licht-Szenario**
- **Anmerkungen**: Farbe, Gerät
- **Absichten**: einschalten, ausschalten, ändern, verringern, erhöhen

#### **Musik-Szenario**
- **Anmerkungen**: Musik, Person, Plattform, Liste
- **Absichten**: spielen, stoppen, pausieren, fortsetzen, abfragen

#### **Wetter-Szenario**
- **Anmerkungen**: Wetterdeskriptor, Ort, Zeit
- **Absichten**: abfragen

#### **API-Szenario** (Wikipedia oder andere Quellen)
- **Anmerkungen**: Thema/Information
- **Absichten**: abfragen

#### **IoT-Szenario**
- **Anmerkungen**: Gerät
- **Absichten**: einschalten, ausschalten, ändern/einstellen, verbinden, abfragen, erhöhen, verringern

#### **System-Szenario** (internal system)
- **Anmerkungen**: Thema
- **Absichten**: pausieren, fortsetzen, erhöhen, verringern

#### **Timer-Szenario**
- **Anmerkungen**: Zeit, Frequenz
- **Absichten**: einstellen, stoppen, entfernen, abfragen

#### **HTW Dresden-Szenario**
- **Anmerkungen**: Thema, ...
- **Absichten**: abfragen

### Python-Klasse: Szenario (Intent)

Die folgende Python-Klasse implementiert das Szenario "List":

```python
class Liste: # Szenario (Class)
    def __init__(self):
        self.Liste = []

    def löschen(self, Artikel, Menge): # Absicht (Funktion) # Anmerkung (Variable) 
        print(f"{Artikel} wurde aus der Liste entfernt")

    def eingeben(self, Artikel, Menge):
        print(f"{Artikel} wurde zur Liste hinzugefügt.")