import utils.api

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