from datetime import datetime, timedelta
import re
import locale
import config

class Datenkonverter:
    def __init__(self):
        locale.setlocale(locale.LC_TIME, config.ZEIT_STANDORT)

    def date_konverter(self, datum):
        if not datum:
            return None, config.ERROR_VARIABLE_DATUM
        jetzt = datetime.now()
        
        if re.search(r"\bheute\b", datum.lower()):
            return jetzt, None
        if re.search(r"\bmorgen\b", datum.lower()):
            return jetzt + timedelta(days=1), None
        if re.search(r"\b[üu]bermorgen\b", datum.lower()):
            return jetzt + timedelta(days=2), None
        if re.search(r"\b(gestern|vorgestern)\b", datum.lower()):
            return jetzt - timedelta(days=1), None
        
        wochentage = {
            "montag": 0, "dienstag": 1, "mittwoch": 2, "donnerstag": 3, 
            "freitag": 4, "samstag": 5, "sonntag": 6
        }
        
        datum_lower = datum.lower()
        if datum_lower in wochentage:
            aktueller_wochentag = jetzt.weekday()
            ziel_wochentag = wochentage[datum_lower]
            
            tage_bis_ziel = (ziel_wochentag - aktueller_wochentag + 7) % 7
            if tage_bis_ziel == 0:
                tage_bis_ziel = 7
                
            return jetzt + timedelta(days=tage_bis_ziel), None
        
        try:
            # dd.mm.yyyy
            return datetime.strptime(datum, "%d.%m.%Y"), None
        except ValueError:
            pass

        try:
            # dd.mm
            if len(datum.split('.')) == 2:
                datum = datum + f".{jetzt.year}"
                return datetime.strptime(datum, "%d.%m.%Y"), None
        except ValueError:
            pass

        try:
            # dd B
            if len(datum.split()) == 2:
                datum = datum + f" {jetzt.year}"
            return datetime.strptime(datum, "%d %B %Y"), None
        
        except ValueError:
            try:
                # dd B ohne y
                datum = datetime.strptime(datum, "%d %B")  
                return datum.replace(year=jetzt.year), None
            except ValueError:
                return None, config.ERROR_VARIABLE_DATUM
                # raise ValueError("Ungültiges Datumsformat. Verwenden Sie 'heute', 'morgen', 'dd.mm', 'dd.mm.yyyy', 'd MMMM' oder 'd MMMM yyyy'.")
    
    def date_zeit_konverter(self, datum, zeit):
        zeitzuordnungen = {
            "morgen": "08:00",
            "mittag": "12:00",
            "nachmittag": "15:00",
            "abend": "18:00",
            "nacht": "22:00",
            "früh": "07:00",
            "spät": "21:00",
            "vormittag": "10:00"
        }
        
        datum, errortyp = self.date_konverter(datum)

        if not datum:
            return None, errortyp
        
        if not zeit:
            return None, config.ERROR_VARIABLE_ZEIT

        # Zeit
        try:
            if zeit.lower() in zeitzuordnungen:
                zeit = zeitzuordnungen[zeit.lower()]
            else:
                if '.' in zeit:
                    zeit = zeit.replace('.', ':')
                zeit_muster = r'\b(\d{1,2}:\d{2}|\d{1,2})\b'
                match = re.search(zeit_muster, zeit)
                if match:
                    zeit = match.group(0)
                    if ":" not in zeit:
                        zeit += ":00"
            
            datum_zeit = datetime.strptime(f"{datum.strftime('%Y-%m-%d')} {zeit}", "%Y-%m-%d %H:%M")
            return datum_zeit.strftime("%Y-%m-%dT%H:%M:%S"), None
        except ValueError:
            return None, config.ERROR_VARIABLE_ZEIT