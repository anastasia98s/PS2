from intents.wetter_intent import WetterIntent
from intents.studienordnung.studienordnung_intent import StudienordnungIntent
from intents.todolist_intent import ToDoListIntent
from intents.wikipedia_intent import WikipediaIntent
from intents.uhrzeit_intent import UhrzeitIntent
from intents.datum_intent import DatumIntent
from neural_network.nn_textklassifizierung.predictor import Predictor as PredictorText
from neural_network.nn_authentifizierung.predictor import Predictor as PredictorUser
from utils.data_controller.user_controller.presenter import PresenterUser
from neural_network.nn_authentifizierung import train as train_merkmale
import config
from utils.audio import Audio
import os
import sys
import warnings
warnings.filterwarnings("ignore")

class Engine:
    def __init__(self):
        self.predictor_text = PredictorText(config.TEXTKLASSIFIZIERUNG_TRAINED_PATH)
        if os.path.exists(config.AUTHENTIFIZIERUNG_TRAINED_PATH):
            self.predictor_user = PredictorUser(config.AUTHENTIFIZIERUNG_TRAINED_PATH)
        else:
            self.predictor_user = None
        
        self.presenter_user = PresenterUser()
        self.wetter_intent = WetterIntent()
        self.studienordnung_intent = StudienordnungIntent()
        self.todolist_intent = ToDoListIntent()
        self.wikipedia_intent = WikipediaIntent()
        self.uhrzeit_intent = UhrzeitIntent()
        self.datum_intent = DatumIntent()
        self.audio = Audio()
    
    def intent_variable_error_reask(self, errortyp, neue_daten_abfragen=False):
        wd_text = "nochmal " if not neue_daten_abfragen else ""
        
        variable_typen = {
            config.ERROR_VARIABLE_DATUM: "das Datum",
            config.ERROR_VARIABLE_ZEIT: "die Zeit",
            config.ERROR_VARIABLE_ORT: "der Ort",
            config.ERROR_VARIABLE_AKTIVITAET: "den Terminnamen oder die Aktivität"
        }

        variable_name = variable_typen.get(errortyp)
        if not variable_name:
            self.audio.text_to_speech("Es gab ein Problem mit dem System. Bitte versuche es erneut.")
            sys.exit("Das Programm wird beendet.")
        return self.dialog(1, f"Kannst du {variable_name} {wd_text}sagen?")
    
    def intent_filter(self, absicht, szenario, anmerkungen, anmerkungen_label, user_id):
        v_satz = []
        v_thema = []
        v_aktivitaet = []
        v_zeit = []
        v_datum = []
        v_ort = []
        for index in range(len(anmerkungen[1])):
            v_satz.append(anmerkungen[1][index])
            match abs(anmerkungen_label[anmerkungen[0][index]]):
                case config.ANMERKUNG_THEMA: # thema
                    v_thema.append(anmerkungen[1][index])
                case config.ANMERKUNG_AKTIVITAET: # aktivitaet name
                    v_aktivitaet.append(anmerkungen[1][index])
                case config.ANMERKUNG_ZEIT: # zeit
                    v_zeit.append(anmerkungen[1][index])
                case config.ANMERKUNG_DATUM: # datum
                    v_datum.append(anmerkungen[1][index])
                case config.ANMERKUNG_ORT: # ort
                    v_ort.append(anmerkungen[1][index])

        t_satz = " ".join(v_satz)
        t_thema = " ".join(v_thema)
        t_aktivitaet = " ".join(v_aktivitaet)
        t_zeit = " ".join(v_zeit)
        t_datum = " ".join(v_datum)
        t_ort = " ".join(v_ort)

        print(f"Satz: {t_satz}")
        print(f"Thema: {t_thema}")
        print(f"Aktivität: {t_aktivitaet}")
        print(f"Zeit: {t_zeit}")
        print(f"Datum: {t_datum}")
        print(f"Ort: {t_ort}")
        print("============================")

        match (szenario, absicht):
            ################################### # zeit
            case (config.SZENARIO_UHRZEIT, config.ABSICHT_ABFRAGEN): # abfragen
                intent_result, error_result = self.uhrzeit_intent.abfragen(t_ort)
                if not error_result:
                    return intent_result
                else:
                    return "Zeit Intent Error!"

            ################################### # datum
            case (config.SZENARIO_DATUM, config.ABSICHT_ABFRAGEN): # abfragen
                while True:
                    intent_result, error_result = self.datum_intent.abfragen(t_datum)
                    if not error_result:
                        return intent_result
                    else:
                        t_datum = self.intent_variable_error_reask(error_result)
                        if any(word in t_datum.lower().split() for word in ["nein", "ne"]):
                            return "verstehe"

            ################################### # wetter
            case (config.SZENARIO_WETTER, config.ABSICHT_ABFRAGEN): # abfragen
                while True:
                    intent_result, error_result = self.wetter_intent.abfragen(t_zeit, t_datum, t_ort)
                    if not error_result:
                        return intent_result
                    else:
                        if error_result == config.ERROR_VARIABLE_DATUM:
                            t_datum = self.intent_variable_error_reask(error_result)
                            if any(word in t_datum.lower().split() for word in ["nein", "ne"]):
                                return "verstehe"
                        elif error_result == config.ERROR_VARIABLE_ZEIT:
                            t_zeit = self.intent_variable_error_reask(error_result)
                            if any(word in t_zeit.lower().split() for word in ["nein", "ne"]):
                                return "verstehe"
                        elif error_result == config.ERROR_VARIABLE_ORT:
                            t_ort = self.intent_variable_error_reask(error_result)
                            if any(word in t_ort.lower().split() for word in ["nein", "ne"]):
                                return "verstehe"

            ################################### # studienordnung
            case (config.SZENARIO_STUDIENORDNUNG, config.ABSICHT_ABFRAGEN): # abfragen
                intent_result, error_result = self.studienordnung_intent.abfragen(t_satz)
                if not error_result:
                    return intent_result
                else:
                    return "Studienordnung Intent Error!"

            ################################### # Wikipedia
            case (config.SZENARIO_WIKIPEDIA, config.ABSICHT_ABFRAGEN): # abfragen
                intent_result, error_result = self.wikipedia_intent.abfragen(t_thema)
                if not error_result:
                    return intent_result
                else:
                    return "Wikipedia Intent Error!"

            ################################### # todo list
            case (config.SZENARIO_TODO_LIST, config.ABSICHT_ABFRAGEN): # abfragen
                while True:
                    intent_result, error_result = self.todolist_intent.abfragen(t_aktivitaet, t_zeit, t_datum, user_id)
                    if not error_result:
                        return intent_result
                    else:
                        if error_result == config.ERROR_VARIABLE_DATUM:
                            t_datum = self.intent_variable_error_reask(error_result)
                            if any(word in t_datum.lower().split() for word in ["nein", "ne"]):
                                return "verstehe"
                        elif error_result == config.ERROR_VARIABLE_ZEIT:
                            t_zeit = self.intent_variable_error_reask(error_result)
                            if any(word in t_zeit.lower().split() for word in ["nein", "ne"]):
                                return "verstehe"
            case (config.SZENARIO_TODO_LIST, config.ABSICHT_EINGEBEN): # hinzufügen
                
                if not t_datum:
                    t_datum = self.intent_variable_error_reask(1, True)
                    if any(word in t_datum.lower().split() for word in ["nein", "ne"]):
                        return "verstehe"
                if not t_zeit:
                    t_zeit = self.intent_variable_error_reask(2, True)
                    if any(word in t_zeit.lower().split() for word in ["nein", "ne"]):
                        return "verstehe"

                while True:
                    intent_result, error_result = self.todolist_intent.eingeben(t_aktivitaet, t_zeit, t_datum, user_id)
                
                    if not error_result:
                        return intent_result
                    else:
                        if error_result == config.ERROR_VARIABLE_DATUM:
                            t_datum = self.intent_variable_error_reask(error_result)
                            if any(word in t_datum.lower().split() for word in ["nein", "ne"]):
                                return "verstehe"
                        elif error_result == config.ERROR_VARIABLE_ZEIT:
                            t_zeit = self.intent_variable_error_reask(error_result)
                            if any(word in t_zeit.lower().split() for word in ["nein", "ne"]):
                                return "verstehe"
                        elif error_result == config.ERROR_VARIABLE_AKTIVITAET:
                            t_aktivitaet = self.intent_variable_error_reask(error_result)
                            if any(word in t_aktivitaet.lower().split() for word in ["nein", "ne"]):
                                return "verstehe"

            case (config.SZENARIO_TODO_LIST, config.ABSICHT_ENTFERNEN): # löschen
                while True:
                    intent_result, error_result = self.todolist_intent.entfernen(t_aktivitaet, t_zeit, t_datum, user_id)
                    if not error_result:
                        return intent_result
                    else:
                        if error_result == config.ERROR_VARIABLE_DATUM:
                            t_datum = self.intent_variable_error_reask(error_result)
                            if any(word in t_datum.lower().split() for word in ["nein", "ne"]):
                                return "verstehe"
                        elif error_result == config.ERROR_VARIABLE_ZEIT:
                            t_zeit = self.intent_variable_error_reask(error_result)
                            if any(word in t_zeit.lower().split() for word in ["nein", "ne"]):
                                return "verstehe"
                        elif error_result == config.ERROR_VARIABLE_AKTIVITAET:
                            t_aktivitaet = self.intent_variable_error_reask(error_result)
                            if any(word in t_aktivitaet.lower().split() for word in ["nein", "ne"]):
                                return "verstehe"
            case _:
                return "Ich verstehe dich nicht."
                        
    def dialog(self, silence_duration, satz):
        self.audio.text_to_speech(satz) # self.audio.text_to_speech(satz)
        _, antwort_text = self.audio.listen_recognize(silence_duration, config.AUDIO_SAMPLE_RATE)
        return antwort_text
    
    def start(self):
        benutzer_id = None
        self.audio.text_to_speech("Ich bin bereit")
        while True:
            antwort_befehl_signal, antwort_befehl_text = self.audio.wake_word_recognize(3, config.AUDIO_SAMPLE_RATE)
            
            if self.predictor_user and benutzer_id is None: # wenn es auth.pth gibt
                name_index, name_label = self.predictor_user.predict(antwort_befehl_signal)
                pred_id = int(name_label[0][name_index][0])
                pred_name = self.presenter_user.show_benutzer_name(pred_id)
                pred_noten = name_label[1][name_index][0]

                if pred_noten < config.AUTHENTIFIZIERUNG_MIN_NOTEN or len(name_label[0]) < config.AUTHENTIFIZIERUNG_MIN_KONTO:
                    antwort_text = self.dialog(0, "Sind Sie " + pred_name)
                    if any(word in antwort_text.lower().split() for word in ["ja", "genau"]):
                        benutzer_id = pred_id
                    else:
                        antwort_text = self.dialog(0, "Haben Sie bereits ein Konto?")
                        if any(word in antwort_text.lower().split() for word in ["ja", "genau"]):
                            for label in name_label[0]:
                                #print(label)
                                geg_id = int(label)
                                geg_name = self.presenter_user.show_benutzer_name(geg_id)
                                antwort_text = self.dialog(0, "Sind Sie " + geg_name)
                                if any(word in antwort_text.lower().split() for word in ["ja", "genau"]):
                                    benutzer_id = geg_id
                                    break
                else:
                    benutzer_id = pred_id

            if not benutzer_id:
                antwort_text = self.dialog(0, "Wollen Sie ein Konto erstellen?")
                
                if any(word in antwort_text.lower().split() for word in ["ja", "okay"]):
                    antwort_text = self.dialog(0.5, "Wie heißt du?")
                    if antwort_text:
                        benutzer_id = self.presenter_user.add_benutzer(antwort_text)
                else:
                    self.audio.text_to_speech("Sie müssen ein Konto haben.")
            
            if benutzer_id:
                self.presenter_user.save_features(antwort_befehl_signal, benutzer_id)
                anmerkung_satz_labels, woerter_anmerkungen, absicht_satz_labels, absicht_class_scores, szenario_satz_labels, szenario_class_scores = self.predictor_text.predict(antwort_befehl_text)
                pred_absicht_noten = absicht_class_scores[1][absicht_satz_labels]
                pred_szenario_noten = szenario_class_scores[1][szenario_satz_labels]
                print("Absichtswahrscheinlichkeit: " + str(pred_absicht_noten) + "/" + str(config.TEXTKLASSIFIZIERUNG_ABSICHT_MIN_NOTEN))
                print("Szenarioswahrscheinlichkeit: " + str(pred_szenario_noten) + "/" + str(config.TEXTKLASSIFIZIERUNG_SZENARIO_MIN_NOTEN))
                if pred_absicht_noten >= config.TEXTKLASSIFIZIERUNG_ABSICHT_MIN_NOTEN and pred_szenario_noten >= config.TEXTKLASSIFIZIERUNG_SZENARIO_MIN_NOTEN:
                    output_satz = self.intent_filter(absicht_class_scores[0][absicht_satz_labels], szenario_class_scores[0][szenario_satz_labels], woerter_anmerkungen, anmerkung_satz_labels, benutzer_id)
                else:
                    output_satz = "Ich verstehe ihren Absicht nicht"
                self.audio.text_to_speech(output_satz)
                if config.AUTHENTIFIZIERUNG_AUTO_TRAINING:
                    train_merkmale.train()

if __name__ == "__main__":
    engine = Engine()
    engine.start()