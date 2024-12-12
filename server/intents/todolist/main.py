import api
import config
from fastapi import FastAPI
from typing import Dict, Any
import uvicorn
from datetime import datetime

app = FastAPI()

def satz_konvertierung(todo_list, todo_datum):
    satze = []
    original_todo_datum = todo_datum
    for item in todo_list:
        id_todo, benutzer_id, todo, datum = item

        if 'T' in datum:
            s_datum, s_zeit = datum.split('T')
            todo_zeit = s_zeit[:5]
            zeit_text, error_request = api.zeit_text_konverter(todo_zeit)
            if error_request:
                return zeit_text
        else:
            s_datum = datum  # Hanya tanggal tanpa waktu
            zeit_text = ""

        if not original_todo_datum:
            # todo_datum = s_datum
            datum_objekt = datetime.fromisoformat(s_datum)
            # datum_objekt = datetime.strptime(s_datum, "%Y-%m-%d")
            if datum_objekt.year == datetime.now().year:
                todo_datum = datum_objekt.strftime("%d. %B")
            else:
                todo_datum = datum_objekt.strftime("%d. %B %Y")

        datum_text, error_request = api.date_text_konverter(todo_datum)
        if error_request:
            return zeit_text
        satze.append(f"Sie haben {datum_text} {zeit_text} {todo}")

    return "\n".join(satze)

@app.post("/todolist_intent/abfragen") 
def abfragen(item: Dict[Any, Any]):
    i_aktivitaet = item.get("aktivitaet")
    i_zeit = item.get("zeit")
    i_datum = item.get("datum")
    i_benutzer_id = item.get("benutzer_id")
    datezeit = None
    datum = None
    t_zeit = None
    t_datum = None
    if i_zeit or i_datum: # Frag nach Aktivität
        t_datum, error_request = api.date_zeit_text_cleaner(i_datum)
        if error_request:
            return t_datum, None
        if i_zeit: # Was habe ich morgen um 12 Uhr
            t_zeit, error_request = api.date_zeit_text_cleaner(i_zeit, is_zeit=True)
            if error_request:
                return t_zeit, None
            datezeit, errortyp, error_request = api.date_zeit_konverter(t_datum, t_zeit)
            if error_request:
                return datezeit, None
            if not datezeit:
                return None, errortyp
        else: # Was habe ich morgen
            datum, errortyp, error_request = api.date_konverter(t_datum)
            if error_request:
                return datum, None
            if not datum:
                return None, errortyp
            else:
                datum = datetime.fromisoformat(datum)
                datum = datum.strftime("%Y-%m-%d")
    
    to_do_liste, error_request = api.show_todo(i_aktivitaet, datum, datezeit, i_benutzer_id)
    if error_request:
        return to_do_liste, None
    if len(to_do_liste):
        t_datum, error_request = api.date_zeit_text_cleaner(i_datum)
        if error_request:
            return t_datum, None
        return satz_konvertierung(to_do_liste, t_datum), None
    else:
        zeit_text, error_request = api.zeit_text_konverter(t_zeit) if t_zeit else ("", None)
        if error_request:
            zeit_text = ""

        datum_text, error_request = api.date_text_konverter(t_datum) if t_datum else ("", None)
        if error_request:
            datum_text = ""

        return f"Sie sind {datum_text} {zeit_text} frei", None

@app.post("/todolist_intent/eingeben") 
def eingeben(item: Dict[Any, Any]):
    i_aktivitaet = item.get("aktivitaet")
    i_zeit = item.get("zeit")
    i_datum = item.get("datum")
    i_benutzer_id = item.get("benutzer_id")
    if i_aktivitaet:
        if not i_datum:
            i_datum = "heute"

        t_datum, error_request = api.date_zeit_text_cleaner(i_datum)
        if error_request:
            return t_datum, None
        if i_zeit:
            t_zeit, error_request = api.date_zeit_text_cleaner(i_zeit, is_zeit=True)
            if error_request:
                return t_zeit, None
            datezeit, errortyp, error_request = api.date_zeit_konverter(t_datum, t_zeit)
            if error_request:
                return datezeit, None
            zeit_text, error_request = api.zeit_text_konverter(t_zeit)
            if error_request:
                return zeit_text, None
        else:
            datezeit, errortyp, error_request = api.date_konverter(t_datum)
            if error_request:
                return datezeit, None
            zeit_text = ""
        
        is_erfolgreich, error_request = api.add_todo(i_aktivitaet, datezeit, i_benutzer_id)
        if error_request:
            return is_erfolgreich, None
        datum_text, error_request = api.date_text_konverter(t_datum)
        if error_request:
            return datum_text, None
        
        return f"neue {i_aktivitaet} {datum_text} {zeit_text} wurde in To-Do-List eingegeben", None
    else:
        return None, api.ERROR_VARIABLE_AKTIVITAET
        # return "Ich kann das To-Do-Objekt nicht identifizieren", None

@app.post("/todolist_intent/entfernen") 
def entfernen(item: Dict[Any, Any]):
    i_aktivitaet = item.get("aktivitaet")
    i_zeit = item.get("zeit")
    i_datum = item.get("datum")
    i_benutzer_id = item.get("benutzer_id")

    datezeit = None
    datum = None
    t_datum = None
    t_zeit = None

    if i_aktivitaet:
        if not i_datum and config.SICHERE_LÖSCHUNG:
            i_datum = "heute"
        if i_datum:
            t_datum, error_request = api.date_zeit_text_cleaner(i_datum)
            if error_request:
                return t_datum, None
            if i_zeit:
                t_zeit, error_request = api.date_zeit_text_cleaner(i_zeit, is_zeit=True)
                if error_request:
                    return t_zeit, None
                datezeit, errortyp, error_request = api.date_zeit_konverter(t_datum, t_zeit)
                if error_request:
                    return datezeit, None
                if not datezeit:
                    return None, errortyp
                
                datum_text, error_request = api.date_text_konverter(t_datum)
                if error_request:
                    return datum_text, None
                zeit_text, error_request = api.zeit_text_konverter(t_zeit)
                if error_request:
                    return zeit_text, None
                antwort = f"{i_aktivitaet} {datum_text} {zeit_text} wurde in To-Do-List gelöscht"
            else:
                datum, errortyp, error_request = api.date_konverter(t_datum)
                if error_request:
                    return datum, None
                if not datum:
                    return None, errortyp
                else:
                    datum = datetime.fromisoformat(datum)
                    datum = datum.strftime("%Y-%m-%d")
                datum_text, error_request = api.date_text_konverter(t_datum)
                if error_request:
                    return datum_text, None
                antwort = f"Alle {i_aktivitaet} {datum_text} wurde in To-Do-List gelöscht"
        else:
            if i_zeit:
                return None, api.ERROR_VARIABLE_DATUM
            datezeit = None
            antwort = f"Alle {i_aktivitaet} wurde in To-Do-List gelöscht"

        is_erfolgreich, error_request = api.delete_todo(i_aktivitaet, datum, datezeit, i_benutzer_id)
        if error_request:
            return is_erfolgreich, None
        if not is_erfolgreich:

            zeit_text, error_request = api.zeit_text_konverter(t_zeit) if t_zeit else ("", None)
            if error_request:
                zeit_text = ""

            datum_text = f"für {t_datum}" if t_datum else ""

            antwort = f"Ich habe kein {i_aktivitaet} {datum_text} {zeit_text} in Ihre To-Do-Liste gefunden"
        
        return antwort, None
    else:
        return None, api.ERROR_VARIABLE_AKTIVITAET
        
if __name__ == "__main__":
    uvicorn.run("main:app", host=api.TODOLIST_INTENT_SERVICE_IP, port=api.TODOLIST_INTENT_SERVICE_PORT)