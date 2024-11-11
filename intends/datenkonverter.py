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
                e_datum = datum + f".{jetzt.year}"
                return datetime.strptime(e_datum, "%d.%m.%Y"), None
        except ValueError:
            pass

        try:
            # dd.mm.
            if len(datum.split('.')) == 3:
                e_datum = datum + str(jetzt.year)
                return datetime.strptime(e_datum, "%d.%m.%Y"), None
        except ValueError:
            pass

        try:
            # dd B (20 Oktober)
            if len(datum.split()) == 2:
                e_datum = datum + f" {jetzt.year}"
                return datetime.strptime(e_datum, "%d %B %Y"), None
        except ValueError:
            pass

        try:
            if len(datum.split()) == 2:
                # dd. B ohne y (20. Oktober)
                e_datum = datum + f" {jetzt.year}"
                return datetime.strptime(e_datum, "%d. %B %Y"), None
        except ValueError:
            pass

        try:
            if len(datum.split()) == 3:
                # dd B yyyy (20 Oktober 2025)
                return datetime.strptime(datum, "%d %B %Y"), None
        except ValueError:
            try:
                # dd. B yyyy (20. Oktober 2025)
                return datetime.strptime(datum, "%d. %B %Y"), None
            except ValueError:
                return None, config.ERROR_VARIABLE_DATUM
            
        return None, config.ERROR_VARIABLE_DATUM
    
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
        
    def date_text_cleaner(self, text, zeit=False):
        text = re.sub(r'\bum\b|\buhr\b', '', text, flags=re.IGNORECASE).strip()
        text = re.sub(r'\bam\b', '', text, flags=re.IGNORECASE).strip()
        text = re.sub(r'\s+', ' ', text).strip()
        if zeit:
            text = text.replace('.', ':')
        return text