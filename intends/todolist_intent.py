from datetime import datetime, timedelta
from data.data_controller.model_user import ModelUser
import re
import locale

class ToDoListIntent:
    def __init__(self):
        self.model_user = ModelUser() # mit Datenbank gebunden

    def date_konvertierung(self, datum):
        locale.setlocale(locale.LC_TIME, 'de_DE.UTF-8')
        jetzt = datetime.now()
        if datum.lower() == "heute":
            return jetzt
        
        if datum.lower() == "morgen":
            return (jetzt + timedelta(days=1))
        
        try:
            # dd.mm.yyyy
            return datetime.strptime(datum, "%d.%m.%Y")
        except ValueError:
            pass

        try:
            # dd.mm
            if len(datum.split('.')) == 2:
                datum = datum + f".{jetzt.year}"  # Tambahkan tahun saat ini
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
                raise ValueError("Ungültiges Datumsformat. Verwenden Sie 'heute', 'morgen', 'dd.mm', 'dd.mm.yyyy', 'd MMMM' oder 'd MMMM yyyy'.")
    
    def date_zeit_konvertierung(self, datum, zeit):
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
        
        datum = self.date_konvertierung(datum)

        # Zeit definieren
        if zeit.lower() in zeitzuordnungen:
            zeit = zeitzuordnungen[zeit.lower()]
        else:
            zeit_muster = r'\b(\d{1,2}:\d{2}|\d{1,2})\b'
            match = re.search(zeit_muster, zeit)
            if match:
                zeit = match.group(0)
                if ":" not in zeit:
                    zeit += ":00"
        
        # Kombiniertes Datum und Zeitformat
        datum_zeit = datetime.strptime(f"{datum.strftime('%Y-%m-%d')} {zeit}", "%Y-%m-%d %H:%M")
        return datum_zeit.strftime("%Y-%m-%dT%H:%M:%S")
    
    def satz_konvertierung(self, todo_list, todo_datum):
        satze = []
        for item in todo_list:
            id_todo, benutzer_id, todo, datum = item

            s_datum, s_zeit = datum.split('T')
            todo_zeit = s_zeit[:5]
            if not todo_datum:
                todo_datum = s_datum

            satze.append(f"Sie haben am {todo_datum} um {todo_zeit} Uhr {todo}")

        return "\n".join(satze)
    
    # Override
    def abfragen(self, i_artikel, i_zeit, i_datum, i_benutzer_id):
        datezeit = None
        datum = None
        if i_zeit or i_datum: # Frag nach Artikel
            if i_zeit: # Was habe ich morgen um 12 Uhr
                datezeit = self.date_zeit_konvertierung(i_datum, i_zeit)
            else: # Was habe ich morgen
                datum = self.date_konvertierung(i_datum).strftime("%Y-%m-%d")
        elif not i_artikel:
            return "Ich verstehe ihre ToDo-Abfrage nicht"
        
        to_do_liste = self.model_user.abfrage_todo(i_artikel, datum, datezeit, i_benutzer_id)
        return self.satz_konvertierung(to_do_liste, i_datum)
    
    # Override
    def eingeben(self, i_artikel, i_zeit, i_datum, i_benutzer_id):
        datezeit = self.date_zeit_konvertierung(i_datum, i_zeit)
        self.model_user.add_todo(i_artikel, datezeit, i_benutzer_id)
        return f"neue {i_artikel} am {i_datum} um {i_zeit} wurde in ToDO Liste eingegeben"
    
    # Override
    def entfernen(self, i_artikel, i_zeit, i_datum, i_benutzer_id):
        if i_datum:
            if i_zeit:
                datezeit = self.date_zeit_konvertierung(i_datum, i_zeit)
                antwort = f"{i_artikel} am {i_datum} um {i_zeit} Uhr wurde in To-Do-List gelöscht"
            else:
                datum = self.date_konvertierung(i_datum).strftime("%Y-%m-%d")
                antwort = f"Alle {i_artikel} am {datum} wurde in To-Do-List gelöscht"
        else:
            datezeit = None
            antwort = f"Alle {i_artikel} wurde in To-Do-List gelöscht"

        self.model_user.delete_todo(i_artikel, i_datum, datezeit, i_benutzer_id)

        return antwort