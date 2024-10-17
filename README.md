# Private Assistant AI

# Datensatz-Szenarien und Absichten

## Listen-Szenario
- **Anmerkungen**: Produkt
- **Absichten**: löschen, eingeben

## Terminplan-Szenario
- **Anmerkungen**: Datum, Uhrzeit, Aufgabe
- **Absichten**: löschen, eingeben

## Termin-Szenario
- **Anmerkungen**: Datum, Uhrzeit, Aufgabe, Ort
- **Absichten**: buchen, stornieren

## Lampen-Szenario
- **Anmerkungen**: Ort
- **Absichten**: dimmen, heller machen, ausschalten, einschalten

## Kamera-Szenario
- **Anmerkungen**: Ort
- **Absichten**: zoom verringern, zoom vergrößern, ausschalten, einschalten, fotografieren, video aufnehmen

## Musik-Szenario
- **Anmerkungen**: Musik, Person
- **Absichten**: abspielen, stoppen, ändern

## Filme-Szenario
- **Anmerkungen**: Film (Name)
- **Absichten**: abspielen, stoppen

## Video-Szenario
- **Anmerkungen**: URL
- **Absichten**: abspielen, stoppen

## URL-Szenario
- **Anmerkungen**: URL
- **Absichten**: öffnen, indizieren

## Nachrichten-Szenario
- **Anmerkungen**: Telefonnummer/WhatsApp, Nachricht, Empfänger
- **Absichten**: senden

## Telefon-Szenario
- **Anmerkungen**: Telefonnummer, Empfänger
- **Absichten**: anrufen

## Wetter-Szenario
- **Anmerkungen**: Datum, Uhrzeit, Ort
- **Absichten**: abfragen

## Nachrichten-Szenario
- **Anmerkungen**: Datum, Kategorie
- **Absichten**: abfragen

## Aktien-Szenario
- **Anmerkungen**: Aktie
- **Absichten**: verkaufen, abfragen, kaufen

## Transport-Szenario
- **Anmerkungen**: Transport (Name, z.B. Taxi)
- **Absichten**: buchen, stornieren

## Alarm-Szenario
- **Anmerkungen**: Datum, Uhrzeit
- **Absichten**: einstellen, entfernen/stoppen

## Audio-Szenario
- **Anmerkungen**: Lautstärke (Zahl)
- **Absichten**: einstellen, verringern, erhöhen

## Wikipedia-Szenario
- **Anmerkungen**: Satz
- **Absichten**: abfragen

## Daten-Szenario
- **Anmerkungen**: Pfad, Datei (z.B. main.py)
- **Absichten**: drucken, lesen, öffnen, löschen, konvertieren

## WLAN-Szenario
- **Anmerkungen**: Netzwerk (WLAN-Name)
- **Absichten**: verbinden, entfernen

## Bluetooth-Szenario
- **Anmerkungen**: Gerät (Gerätename)
- **Absichten**: verbinden, entfernen

## Berechnung-Szenario
- **Anmerkungen**: Zahl, Operator
- **Absichten**: berechnen

## Wiederholung-Szenario
- **Anmerkungen**: (letzte gespeicherte Absicht)
- **Absichten**: wiederholen

## Timer-Szenario
- **Anmerkungen**: Uhrzeit
- **Absichten**: einstellen

## Alarm-Szenario
- **Anmerkungen**: Datum, Uhrzeit
- **Absichten**: einstellen

### Python-Klasse: Szenario (Intent)

Die folgende Python-Klasse implementiert das Szenario "List":

```python
class List:
    def __init__(self, produkt, lst):
        self.produkt = produkt
        self.lst = lst

    def löschen(self):
        if self.produkt in self.lst:
            self.lst.remove(self.produkt)
            print(f"{self.produkt} wurde aus der Liste entfernt.")
        else:
            print(f"{self.produkt} ist nicht in der Liste enthalten.")

    def eingeben(self, neues_produkt):
        self.lst.append(neues_produkt)
        print(f"{neues_produkt} wurde zur Liste hinzugefügt.")