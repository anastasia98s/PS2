import config
from aktivierungswort.aktivierungswort_controller.presenter import PresenterAktivierungswort
from aktivierungswort.nn_aktivierungswort import train
import utils.api
from utils.utils import anmerkungen_inhalt_extrahieren
import re
import csv
import tkinter as tk
from tkinter import filedialog

def intent_filter(absicht, szenario, anmerkungen, anmerkungen_label, user_id):
    t_satz, t_thema, t_aktivitaet, t_zeit, t_datum, t_ort = anmerkungen_inhalt_extrahieren(anmerkungen, anmerkungen_label)

    match (szenario, absicht):
        case (utils.api.SZENARIO_UHRZEIT, utils.api.ABSICHT_ABFRAGEN):
            intent_result, error_result = utils.api.uhrzeit_intent_abfragen(t_ort)
        case (utils.api.SZENARIO_DATUM, utils.api.ABSICHT_ABFRAGEN):
            intent_result, error_result = utils.api.datum_intent_abfragen(t_datum)
        case (utils.api.SZENARIO_WETTER, utils.api.ABSICHT_ABFRAGEN):
            intent_result, error_result = utils.api.wetter_intent_abfragen(t_zeit, t_datum, t_ort)
        case (utils.api.SZENARIO_STUDIENORDNUNG, utils.api.ABSICHT_ABFRAGEN):
            intent_result, error_result = utils.api.studienordnung_intent_abfragen(t_satz)
        case (utils.api.SZENARIO_WIKIPEDIA, utils.api.ABSICHT_ABFRAGEN):
            intent_result, error_result = utils.api.wikipedia_intent_abfragen(t_thema)
        case (utils.api.SZENARIO_TODO_LIST, utils.api.ABSICHT_ABFRAGEN): # abfragen
            intent_result, error_result = utils.api.todolist_intent_abfragen(t_aktivitaet, t_zeit, t_datum, user_id)
        case (utils.api.SZENARIO_TODO_LIST, utils.api.ABSICHT_EINGEBEN): # hinzufügen
            intent_result, error_result = utils.api.todolist_intent_eingeben(t_aktivitaet, t_zeit, t_datum, user_id)
        case (utils.api.SZENARIO_TODO_LIST, utils.api.ABSICHT_ENTFERNEN): # löschen
            intent_result, error_result = utils.api.todolist_intent_entfernen(t_aktivitaet, t_zeit, t_datum, user_id)
        case (utils.api.SZENARIO_SYSTEM, utils.api.ABSICHT_ZURUECKGEHEN):
            intent_result, error_result = "Öffne die vorherige Playlist", None
        case (utils.api.SZENARIO_SYSTEM, utils.api.ABSICHT_WEITERGEHEN):
            intent_result, error_result = "Öffne eine andere Playlist", None
        case (utils.api.SZENARIO_SYSTEM, utils.api.ABSICHT_WIEDERHOLEN):
            intent_result, error_result = "Die Webseite wurde erfolgreich aktualisiert", None
        case (utils.api.SZENARIO_SYSTEM, utils.api.ABSICHT_ABBRECHEN):
            intent_result, error_result = "Die Website wurde geschlossen", None
        case (utils.api.SZENARIO_YOUTUBE, utils.api.ABSICHT_ABFRAGEN):
            intent_result, error_result, error_request = utils.api.youtube_intent_abfragen(t_thema)
            if not error_result and not error_request:
                if intent_result:
                    intent_result, error_result = f"Ich habe {intent_result[0][0]} in Youtube gefunden", None
                else:
                    intent_result, error_result = f"Ich habe kein Video über {t_thema} in Youtube gefunden", None
                                    
        case (utils.api.SZENARIO_SEARCH_ENGINE, utils.api.ABSICHT_ABFRAGEN): # abfragen
            intent_result, error_result, error_request = utils.api.search_engine_intent_abfragen(t_thema)
            if not error_result and not error_request:
                if intent_result:
                    intent_result, error_result = f"Ich habe {intent_result[0][0]} in Google gefunden", None
                else:
                    intent_result, error_result = f"Ich habe kein Thema über {t_thema} in Google gefunden", None
        case _:
            intent_result, error_result = "Ich verstehe ihren Absicht nicht!", None
    if error_result:
        return "Test kann nicht ausgeführt werden, es fehlen Variablen!", 1
    else:
        return intent_result, None

root = tk.Tk()
root.withdraw()
def save_csv_file(data, label, fname):
    try:
        print("- Wenn der Popup-Ordner nicht erscheint, schau mal im Hintergrund!")
        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv"), ("All Files", "*.*")], initialfile=f"{fname}.csv")
        if file_path:
            with open(file_path, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(label)
                writer.writerows(data)
            print(f"Speicherpfad: {file_path}")
        else:
            print("Speichern abgebrochen")
    except Exception as e:
        print(f"Error: {e}")

def verlauf_anzeigen():
    res_show_verlauf, error_request = utils.api.show_verlauf()
    if not error_request:
        if res_show_verlauf:
            print("=" * 20)
            for item in res_show_verlauf:
                print(f"\nID\t: {item[0]}\nIntent\t: {item[1]} {item[2]}\nEingabe\t: {item[3]}\nAusgabe\t: {item[4]}\nNote\t: {item[5]}\n")
            print("=" * 20)
            return None
        else:
            print("- Verlaufsdatenbak ist leer!")
            return 1
    else:
        print("- Es liegt ein Fehler auf dem Server vor!")
        return 1

def main():
    while True:
        print("\nBitte wähle eine Option:")
        print("1. AI Aktivierungswort")
        print("2. Testprogramm")
        print("3. Beenden")
        auswahl = input("Gib die Nummer der Option ein: ")
        
        if auswahl == '1':
            presenter = PresenterAktivierungswort()
            while True:
                print("\n==Aktivierungswort")
                print("Bitte wähle eine Option:")
                print("1. Aktivierungswort aufnehmen")
                print("2. Aktivierungswort-AI Training")
                print("3. züruck")
                auswahl = input("Gib die Nummer der Option ein: ")
                
                if auswahl == '1':
                    presenter.aktivierungswort_aufnehmen(config.AKTIVIERUNGSWORT_AUFNAHME_DAUER, utils.api.AUDIO_SAMPLE_RATE)
                if auswahl == '2':
                    train.train()
                if auswahl == '3':
                    break
        elif auswahl == '2':
            while True:
                print("\n==Testprogramm")
                print("Bitte wähle eine Option:")
                print("1. Chat")
                print("2. als CSV speichern")
                print("3. Verläufe anzeigen")
                print("4. Verlauf löschen")
                print("5. züruck")
                auswahl = input("Gib die Nummer der Option ein: ")
                if auswahl == '1':
                    print("\n==Chat")
                    test_benutzer_id, error_request = utils.api.add_benutzer("test user")
                    print("\n\n!Dies ist nur ein Testprogramm, viele Funktionen fehlen und die Antworten sind nicht so gut wie im Originalprogramm!\n")
                    
                    verlauf_input = input("Wollen Sie den Verlauf in Server speichern? (y/n): ").strip().lower()
                    if verlauf_input in ('y', 'n'):
                        print("„quit“ zum Beenden\n")
                        while True:
                            print("\n" + "="* 30)
                            chat_input = input("You\t: ")
                            if chat_input == "quit": break
                            textklassifizierung_data, error_request = utils.api.predictor_text_predict(re.sub(r'[.!?]+$', '', chat_input))

                            if not error_request:
                                anmerkung_satz_labels = textklassifizierung_data["anmerkung_satz_labels"]
                                woerter_anmerkungen = textklassifizierung_data["woerter_anmerkungen"]
                                absicht_satz_labels = textklassifizierung_data["absicht_satz_labels"]
                                absicht_class_scores = textklassifizierung_data["absicht_class_scores"]
                                szenario_satz_labels = textklassifizierung_data["szenario_satz_labels"]
                                szenario_class_scores = textklassifizierung_data["szenario_class_scores"]
                                
                                pred_absicht_noten = absicht_class_scores[1][absicht_satz_labels]
                                pred_szenario_noten = szenario_class_scores[1][szenario_satz_labels]
                                if pred_absicht_noten >= config.TEXTKLASSIFIZIERUNG_ABSICHT_MIN_NOTEN and pred_szenario_noten >= config.TEXTKLASSIFIZIERUNG_SZENARIO_MIN_NOTEN:
                                    output_satz, error_output = intent_filter(absicht_class_scores[0][absicht_satz_labels], szenario_class_scores[0][szenario_satz_labels], woerter_anmerkungen, anmerkung_satz_labels, test_benutzer_id)
                                    output_satz = " ".join(output_satz.splitlines())
                                else:
                                    print(f"=> Absichtswahrscheinlichkeit: {pred_absicht_noten}/{config.TEXTKLASSIFIZIERUNG_ABSICHT_MIN_NOTEN} | => Szenarioswahrscheinlichkeit: {pred_szenario_noten}/{config.TEXTKLASSIFIZIERUNG_SZENARIO_MIN_NOTEN}")
                                    output_satz, error_output = (f"Ich bin für diese Absicht noch nicht trainiert!", None)
                            else:
                                output_satz, error_output = textklassifizierung_data, 1

                            print("AI\t:", output_satz)
                            if not error_output and verlauf_input == "y":
                                print("\nBitte bewerten Sie die Ausgabe auf einer Skala von 1 (beste) bis 5 (schlechteste):\n"
                                        "0 - nicht speichern")
                                while True:
                                    try:
                                        note_input = int(input("- Note: "))
                                        if 0 <= note_input <= 5:
                                            if note_input != 0:
                                                res_add_verlauf, error_request = utils.api.add_verlauf(szenario_class_scores[0][szenario_satz_labels], absicht_class_scores[0][absicht_satz_labels], chat_input, output_satz, note_input)
                                                if error_request:
                                                    print(f"- {str(res_add_verlauf)}\n")
                                                else:
                                                    print("- Der Verlauf wurde gespeichert!\n")
                                            else:
                                                print("- Der Verlauf wurde nicht gespeichert!\n")
                                            break
                                    except ValueError:
                                        print("!!Ungültige Eingabe. Bitte 0 bis 5 eingeben!!")
                    else:
                        print("Ungültige Eingabe. Bitte 'y' oder 'n' eingeben.")
                elif auswahl == '2':
                    print("\n==als CSV speichern")
                    res_show_verlauf, error_request = utils.api.show_verlauf()
                    if not error_request:
                        if res_show_verlauf:
                            res_show_verlauf_ohne_id = [item[1:] for item in res_show_verlauf]
                            save_csv_file(res_show_verlauf_ohne_id, ["Szenario", "Absicht", "Eingabe", "Ausgabe", "Note"], "verlauf_data")
                        else:
                            print("- Verlaufsdatenbak ist leer!")
                    else:
                        print("- Es liegt ein Fehler auf dem Server vor!")
                elif auswahl == '3':
                    print("\n==Verläufe anzeigen")
                    _ = verlauf_anzeigen()
                elif auswahl == '4':
                    verlauf_anzeigen_leer = verlauf_anzeigen()
                    if not verlauf_anzeigen_leer:
                        print("\n==Verlauf löschen")
                        print("0 - züruck")
                        delete_input = input("ID: ")
                        if delete_input.isdigit():
                            if delete_input != '0':
                                delete_result, delete_error, error_request = utils.api.delete_verlauf(delete_input)
                                print(f"- {str(delete_result)}")
                        else:
                            print("- !!Ungültige Eingabe!!")
                elif auswahl == '5':
                    break
                else:
                    print("- Ungültige Auswahl, bitte versuche es erneut.")
        elif auswahl == '3':
            break
        else:
            print("- Ungültige Auswahl, bitte versuche es erneut.")

if __name__ == "__main__":
    main()