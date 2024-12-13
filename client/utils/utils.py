import utils.api

def reask_text(errortyp, neue_daten_abfragen=False):
    wd_text = "nochmal " if not neue_daten_abfragen else ""
    variable_typen = {
        utils.api.ERROR_VARIABLE_DATUM: "ein genaues Datum",
        utils.api.ERROR_VARIABLE_ZEIT: "eine genaue Zeit",
        utils.api.ERROR_VARIABLE_ORT: "der Ort",
        utils.api.ERROR_VARIABLE_AKTIVITAET: "eine genaue Aktivität",
        utils.api.ERROR_VARIABLE_THEMA: "das Thema"
    }

    variable_name = variable_typen.get(errortyp)
    if not variable_name:
        return "Es gab ein Problem mit dem System. Bitte versuche es erneut", 1
    else:
        return f"Kannst du {variable_name} {wd_text}sagen?", None

def anmerkungen_inhalt_extrahieren(anmerkungen, anmerkungen_label):
    v_satz = []
    v_thema = []
    v_aktivitaet = []
    v_zeit = []
    v_datum = []
    v_ort = []
    
    for index in range(len(anmerkungen[1])):
        v_satz.append(anmerkungen[1][index])
        match abs(anmerkungen_label[anmerkungen[0][index]]):
            case utils.api.ANMERKUNG_THEMA: # thema
                v_thema.append(anmerkungen[1][index])
            case utils.api.ANMERKUNG_AKTIVITAET: # aktivitaet name
                v_aktivitaet.append(anmerkungen[1][index])
            case utils.api.ANMERKUNG_ZEIT: # zeit
                v_zeit.append(anmerkungen[1][index])
            case utils.api.ANMERKUNG_DATUM: # datum
                v_datum.append(anmerkungen[1][index])
            case utils.api.ANMERKUNG_ORT: # ort
                v_ort.append(anmerkungen[1][index])

    t_satz = " ".join(v_satz)
    t_thema = " ".join(v_thema)
    t_aktivitaet = " ".join(v_aktivitaet)
    t_zeit = " ".join(v_zeit)
    t_datum = " ".join(v_datum)
    t_ort = " ".join(v_ort)

    #print("\n============================")
    #print(f"Satz: {t_satz}")
    #print(f"Thema: {t_thema}")
    #print(f"Aktivität: {t_aktivitaet}")
    #print(f"Zeit: {t_zeit}")
    #print(f"Datum: {t_datum}")
    #print(f"Ort: {t_ort}")
    #print("============================\n")

    return t_satz, t_thema, t_aktivitaet, t_zeit, t_datum, t_ort