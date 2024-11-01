from data.data_controller.model_user import ModelUser
from intends.datenkonverter import Datenkonverter
import config

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
    
    def abfragen(self, i_aktivitaet, i_zeit, i_datum, i_benutzer_id):
        datezeit = None
        datum = None
        if i_zeit or i_datum: # Frag nach Aktivität
            if i_zeit: # Was habe ich morgen um 12 Uhr
                datezeit, errortyp = super().date_zeit_konverter(i_datum, i_zeit)
                if not datezeit:
                    return None, errortyp
            else: # Was habe ich morgen
                datum, errortyp = super().date_konverter(i_datum)
                if not datum:
                    return None, errortyp
                else:
                    datum = datum.strftime("%Y-%m-%d")
        elif not i_aktivitaet:
            return "Ich verstehe ihre To-Do-Abfrage nicht", None
        
        to_do_liste = self.model_user.abfrage_todo(i_aktivitaet, datum, datezeit, i_benutzer_id)
        if len(to_do_liste):
            return self.satz_konvertierung(to_do_liste, i_datum), None
        else:
            return "Sie sind frei", None
    
    def eingeben(self, i_aktivitaet, i_zeit, i_datum, i_benutzer_id):
        if i_aktivitaet:
            datezeit, errortyp = super().date_zeit_konverter(i_datum, i_zeit)
            if not datezeit:
                return None, errortyp
            self.model_user.add_todo(i_aktivitaet, datezeit, i_benutzer_id)
            return f"neue {i_aktivitaet} am {i_datum} um {i_zeit} wurde in To-Do-List eingegeben", None
        else:
            return None, config.ERROR_VARIABLE_AKTIVITAET
            # return "Ich kann das To-Do-Objekt nicht identifizieren", None
    
    def entfernen(self, i_aktivitaet, i_zeit, i_datum, i_benutzer_id):
        datezeit = None
        datum = None
        if i_aktivitaet:
            if i_datum:
                if i_zeit:
                    datezeit, errortyp = super().date_zeit_konverter(i_datum, i_zeit)
                    if not datezeit:
                        return None, errortyp
                    antwort = f"{i_aktivitaet} am {i_datum} um {i_zeit} Uhr wurde in To-Do-List gelöscht"
                else:
                    datum, errortyp = super().date_konverter(i_datum)
                    if not datum:
                        return None, errortyp
                    else:
                        datum = datum.strftime("%Y-%m-%d")
                    antwort = f"Alle {i_aktivitaet} am {i_datum} wurde in To-Do-List gelöscht"
            else:
                datezeit = None
                antwort = f"Alle {i_aktivitaet} wurde in To-Do-List gelöscht"

            delete_result = self.model_user.delete_todo(i_aktivitaet, datum, datezeit, i_benutzer_id)
            if not delete_result:
                antwort = f"Ich habe kein {i_aktivitaet} in Ihre To-Do-Liste gefunden"
                
            return antwort, None
        else:
            return None, config.ERROR_VARIABLE_AKTIVITAET