from data.data_controller.model_user import ModelUser
from intends.datenkonverter import Datenkonverter
import config
from datetime import datetime

class ToDoListIntent(Datenkonverter):
    def __init__(self):
        super().__init__()
        self.model_user = ModelUser() # mit Datenbank verbinden
    
    def satz_konvertierung(self, todo_list, todo_datum):
        satze = []
        original_todo_datum = todo_datum
        for item in todo_list:
            id_todo, benutzer_id, todo, datum = item

            s_datum, s_zeit = datum.split('T')
            todo_zeit = s_zeit[:5]
            if not original_todo_datum:
                # todo_datum = s_datum
                datum_objekt = datetime.strptime(s_datum, "%Y-%m-%d")
                if datum_objekt.year == datetime.now().year:
                    todo_datum = datum_objekt.strftime("%d. %B")
                else:
                    todo_datum = datum_objekt.strftime("%d. %B %Y")

            satze.append(f"Sie haben am {todo_datum} um {todo_zeit} Uhr {todo}")

        return "\n".join(satze)
    
    def abfragen(self, i_aktivitaet, i_zeit, i_datum, i_benutzer_id):
        datezeit = None
        datum = None
        if i_zeit or i_datum: # Frag nach Aktivität
            t_datum = super().date_text_cleaner(i_datum)
            if i_zeit: # Was habe ich morgen um 12 Uhr
                t_zeit = super().date_text_cleaner(i_zeit, zeit=True)
                datezeit, errortyp = super().date_zeit_konverter(t_datum, t_zeit)
                if not datezeit:
                    return None, errortyp
            else: # Was habe ich morgen
                datum, errortyp = super().date_konverter(t_datum)
                if not datum:
                    return None, errortyp
                else:
                    datum = datum.strftime("%Y-%m-%d")
        
        to_do_liste = self.model_user.show_todo(i_aktivitaet, datum, datezeit, i_benutzer_id)
        if len(to_do_liste):
            t_datum = super().date_text_cleaner(i_datum)
            return self.satz_konvertierung(to_do_liste, t_datum), None
        else:
            return "Sie sind frei", None
    
    def eingeben(self, i_aktivitaet, i_zeit, i_datum, i_benutzer_id):
        if i_aktivitaet:
            t_datum = super().date_text_cleaner(i_datum)
            t_zeit = super().date_text_cleaner(i_zeit, zeit=True)
            datezeit, errortyp = super().date_zeit_konverter(t_datum, t_zeit)
            if not datezeit:
                return None, errortyp
            self.model_user.add_todo(i_aktivitaet, datezeit, i_benutzer_id)
            return f"neue {i_aktivitaet} am {t_datum} um {t_zeit} wurde in To-Do-List eingegeben", None
        else:
            return None, config.ERROR_VARIABLE_AKTIVITAET
            # return "Ich kann das To-Do-Objekt nicht identifizieren", None
    
    def entfernen(self, i_aktivitaet, i_zeit, i_datum, i_benutzer_id):
        datezeit = None
        datum = None
        if i_aktivitaet:
            if i_datum:
                t_datum = super().date_text_cleaner(i_datum)
                if i_zeit:
                    t_zeit = super().date_text_cleaner(i_zeit, zeit=True)
                    datezeit, errortyp = super().date_zeit_konverter(t_datum, t_zeit)
                    if not datezeit:
                        return None, errortyp
                    antwort = f"{i_aktivitaet} am {t_datum} um {t_zeit} Uhr wurde in To-Do-List gelöscht"
                else:
                    datum, errortyp = super().date_konverter(t_datum)
                    if not datum:
                        return None, errortyp
                    else:
                        datum = datum.strftime("%Y-%m-%d")
                    antwort = f"Alle {i_aktivitaet} am {t_datum} wurde in To-Do-List gelöscht"
            else:
                datezeit = None
                antwort = f"Alle {i_aktivitaet} wurde in To-Do-List gelöscht"

            delete_result = self.model_user.delete_todo(i_aktivitaet, datum, datezeit, i_benutzer_id)
            if not delete_result:
                antwort = f"Ich habe kein {i_aktivitaet} in Ihre To-Do-Liste gefunden"
                
            return antwort, None
        else:
            return None, config.ERROR_VARIABLE_AKTIVITAET