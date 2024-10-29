from data.data_controller.model_user import ModelUser
from intends.datenkonverter import Datenkonverter

class ToDoListIntent(Datenkonverter):
    def __init__(self):
        self.model_user = ModelUser() # mit Datenbank gebunden
    
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
    
    def abfragen(self, i_artikel, i_zeit, i_datum, i_benutzer_id):
        datezeit = None
        datum = None
        if i_zeit or i_datum: # Frag nach Artikel
            if i_zeit: # Was habe ich morgen um 12 Uhr
                datezeit = super().date_zeit_konverter(i_datum, i_zeit)
                if not datezeit:
                    return None
            else: # Was habe ich morgen
                datum = super().date_konverter(i_datum)
                if not datum:
                    return None
                else:
                    datum = datum.strftime("%Y-%m-%d")
        elif not i_artikel:
            return "Ich verstehe ihre To-Do-Abfrage nicht"
        
        to_do_liste = self.model_user.abfrage_todo(i_artikel, datum, datezeit, i_benutzer_id)
        return self.satz_konvertierung(to_do_liste, i_datum)
    
    def eingeben(self, i_artikel, i_zeit, i_datum, i_benutzer_id):
        datezeit = super().date_zeit_konverter(i_datum, i_zeit)
        if not datezeit:
            return None
        self.model_user.add_todo(i_artikel, datezeit, i_benutzer_id)
        return f"neue {i_artikel} am {i_datum} um {i_zeit} wurde in To-Do-List eingegeben"
    
    def entfernen(self, i_artikel, i_zeit, i_datum, i_benutzer_id):
        if i_datum:
            if i_zeit:
                datezeit = super().date_zeit_konverter(i_datum, i_zeit)
                if not datezeit:
                    return None
                antwort = f"{i_artikel} am {i_datum} um {i_zeit} Uhr wurde in To-Do-List gelöscht"
            else:
                datum = super().date_konverter(i_datum)
                if not datum:
                    return None
                else:
                    datum = datum.strftime("%Y-%m-%d")
                antwort = f"Alle {i_artikel} am {datum} wurde in To-Do-List gelöscht"
        else:
            datezeit = None
            antwort = f"Alle {i_artikel} wurde in To-Do-List gelöscht"

        self.model_user.delete_todo(i_artikel, i_datum, datezeit, i_benutzer_id)

        return antwort