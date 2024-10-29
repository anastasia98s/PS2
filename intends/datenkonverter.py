from datetime import datetime, timedelta
import re
import locale
import config

class Datenkonverter:
    def __init__(self):
        locale.setlocale(locale.LC_TIME, config.ZEIT_STANDORT)

    def date_konverter(self, datum):
        jetzt = datetime.now()
        
        if re.search(r"\bheute\b", datum.lower()):
            return jetzt
        if re.search(r"\bmorgen\b", datum.lower()):
            return jetzt + timedelta(days=1)
        if re.search(r"\b[üu]bermorgen\b", datum.lower()):
            return jetzt + timedelta(days=2)
        if re.search(r"\bgestern\b", datum.lower()):
            return jetzt - timedelta(days=1)
        
        try:
            # dd.mm.yyyy
            return datetime.strptime(datum, "%d.%m.%Y")
        except ValueError:
            pass

        try:
            # dd.mm
            if len(datum.split('.')) == 2:
                datum = datum + f".{jetzt.year}"
                return datetime.strptime(datum, "%d.%m.%Y")
        except ValueError:
            pass

        try:
            # dd B
            if len(datum.split()) == 2:
                datum = datum + f" {jetzt.year}"
            return datetime.strptime(datum, "%d %B %Y")
        
        except ValueError:
            try:
                # dd B ohne y
                datum = datetime.strptime(datum, "%d %B")  
                return datum.replace(year=jetzt.year)
            except ValueError:
                return None
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
        
        datum = self.date_konverter(datum)

        if not datum:
            return None

        # Zeit
        if zeit.lower() in zeitzuordnungen:
            zeit = zeitzuordnungen[zeit.lower()]
        else:
            zeit_muster = r'\b(\d{1,2}:\d{2}|\d{1,2})\b'
            match = re.search(zeit_muster, zeit)
            if match:
                zeit = match.group(0)
                if ":" not in zeit:
                    zeit += ":00"
        
        datum_zeit = datetime.strptime(f"{datum.strftime('%Y-%m-%d')} {zeit}", "%Y-%m-%d %H:%M")
        return datum_zeit.strftime("%Y-%m-%dT%H:%M:%S")