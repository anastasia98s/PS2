from intends.wetter_intent import WetterIntent
from intends.studienordnung_intent import StudienordnungIntent
from intends.todolist_intent import ToDoListIntent
from intends.wikipedia_intent import WikipediaIntent
from intends.uhrzeit_intent import UhrzeitIntent
from intends.datum_intent import DatumIntent
from nn_authentifizierung.utils import extract_features
from nn_textklassifizierung.predictor import Predictor as PredictorText
from nn_authentifizierung.predictor import Predictor as PredictorUser
from data.data_controller.model_user import ModelUser
from nn_authentifizierung import train as train_merkmale
import config
from utils.audio import Audio
import os
import sys


class Engine:
    def __init__(self):
        self.predictor_text = PredictorText(config.TEXTKLASSIFIZIERUNG_TRAINED_PATH)
        if os.path.exists(config.AUTHENTIFIZIERUNG_TRAINED_PATH):
            self.predictor_user = PredictorUser(config.AUTHENTIFIZIERUNG_TRAINED_PATH)
        else:
            self.predictor_user = None
        self.model_user = ModelUser()
        self.wetter_intent = WetterIntent()
        self.studienordnung_intent = StudienordnungIntent()
        self.todolist_intent = ToDoListIntent()
        self.wikipedia_intent = WikipediaIntent()
        self.uhrzeit_intent = UhrzeitIntent()
        self.datum_intent = DatumIntent()
        self.audio = Audio()

    """ def satz_klassifizieren(self, text):
        return self.predictor_text.predict(text) """
    
    def user_authentifizierung(self, signal):
        name_indexs, name_label_scores = self.predictor_user.predict(signal)
        return name_indexs, name_label_scores
    
    def intent_variable_error_reask(self, errortyp):
        if errortyp == config.ERROR_VARIABLE_DATUM:
            return self.dialog("Kannst du das Datum nochmal sagen")
        elif errortyp == config.ERROR_VARIABLE_ZEIT:
            return self.dialog("Kannst du die Zeit nochmal sagen")
        elif errortyp == config.ERROR_VARIABLE_ORT:
            return self.dialog("Kannst du das Ort nochmal sagen")
        elif errortyp == config.ERROR_VARIABLE_ARTIKEL:
            return self.dialog("Kannst du den Artikel nochmal sagen")
        else:
            self.audio.text_to_speech("Es gab ein Problem mit dem System. Bitte versuche es erneut.", config.RECORD_ANTWORT_TMP_PATH)
            sys.exit("Das Programm wird beendet.")
    
    def intent_filter(self, absicht, szenario, anmerkungen, anmerkungen_label, user_id):
        v_thema = []
        v_artikel = []
        v_zeit = []
        v_datum = []
        v_ort = []
        # print(absicht, szenario)
        for index in range(len(anmerkungen[1])):
            # print(anmerkungen[1][index], anmerkungen_label[anmerkungen[0][index]])
            match anmerkungen_label[anmerkungen[0][index]]:
                case config.ANMERKUNG_THEMA: # thema
                    v_thema.append(anmerkungen[1][index])
                case config.ANMERKUNG_ARTIKEL: # artikel name
                    v_artikel.append(anmerkungen[1][index])
                case config.ANMERKUNG_ZEIT: # zeit
                    v_zeit.append(anmerkungen[1][index])
                case config.ANMERKUNG_DATUM: # datum
                    v_datum.append(anmerkungen[1][index])
                case config.ANMERKUNG_ORT: # ort
                    v_ort.append(anmerkungen[1][index])

        t_thema = " ".join(v_thema)
        t_artikel = " ".join(v_artikel)
        t_zeit = " ".join(v_zeit)
        t_datum = " ".join(v_datum)
        t_ort = " ".join(v_ort)
        print("============================", t_zeit, t_datum)
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

            ################################### # wetter
            case (config.SZENARIO_WETTER, config.ABSICHT_ABFRAGEN): # abfragen
                while True:
                    intent_result, error_result = self.wetter_intent.abfragen(t_zeit, t_datum, t_ort)
                    if not error_result:
                        return intent_result
                    else:
                        if error_result == config.ERROR_VARIABLE_DATUM:
                            t_datum = self.intent_variable_error_reask(error_result)
                        elif error_result == config.ERROR_VARIABLE_ZEIT:
                            t_zeit = self.intent_variable_error_reask(error_result)
                        elif error_result == config.ERROR_VARIABLE_ORT:
                            t_ort = self.intent_variable_error_reask(error_result)

            ################################### # studienordnung
            case (config.SZENARIO_STUDIENORDNUNG, config.ABSICHT_ABFRAGEN): # abfragen
                intent_result, error_result = self.studienordnung_intent.abfragen(t_thema)
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
                    intent_result, error_result = self.todolist_intent.abfragen(t_artikel, t_zeit, t_datum, user_id)
                    if not error_result:
                        return intent_result
                    else:
                        if error_result == config.ERROR_VARIABLE_DATUM:
                            t_datum = self.intent_variable_error_reask(error_result)
                        elif error_result == config.ERROR_VARIABLE_ZEIT:
                            t_zeit = self.intent_variable_error_reask(error_result)
            case (config.SZENARIO_TODO_LIST, config.ABSICHT_EINGEBEN): # hinzufügen
                
                if not t_datum:
                    t_datum = self.intent_variable_error_reask(1)
                if not t_zeit:
                    t_zeit = self.intent_variable_error_reask(2)

                while True:
                    intent_result, error_result = self.todolist_intent.eingeben(t_artikel, t_zeit, t_datum, user_id)
                
                    if not error_result:
                        return intent_result
                    else:
                        if error_result == config.ERROR_VARIABLE_DATUM:
                            t_datum = self.intent_variable_error_reask(error_result)
                        elif error_result == config.ERROR_VARIABLE_ZEIT:
                            t_zeit = self.intent_variable_error_reask(error_result)

            case (config.SZENARIO_TODO_LIST, config.ABSICHT_ENTFERNEN): # löschen
                while True:
                    intent_result, error_result = self.todolist_intent.entfernen(t_artikel, t_zeit, t_datum, user_id)
                    if not error_result:
                        return intent_result
                    else:
                        if error_result == config.ERROR_VARIABLE_DATUM:
                            t_datum = self.intent_variable_error_reask(error_result)
                        elif error_result == config.ERROR_VARIABLE_ZEIT:
                            t_zeit = self.intent_variable_error_reask(error_result)
                        elif error_result == config.ERROR_VARIABLE_ARTIKEL:
                            t_artikel = self.intent_variable_error_reask(error_result)
            case _:
                return "Ich verstehe dich nicht."
            
    def save_features(self, signal, benutzer_id):
        target_length = config.AUDIO_SIGNAL_LENGTH_SAVE
        signal_length = len(signal)
        num_parts = (signal_length - target_length) // target_length
        
        for i in range(num_parts):
            signal_part = signal[i * target_length : (i + 1) * target_length]
            features = extract_features(signal_part, config.AUTHENTIFIZIERUNG_SAMPLE_RATE)
            self.model_user.add_merkmale(benutzer_id, features)
        
        remainder_length = signal_length % target_length
        if remainder_length > 0:
            signal_part = signal[num_parts * target_length:]
            features = extract_features(signal_part, config.AUTHENTIFIZIERUNG_SAMPLE_RATE)
            self.model_user.add_merkmale(benutzer_id, features)
            
    def dialog(self, satz):
        self.audio.text_to_speech(satz, config.RECORD_ANTWORT_TMP_PATH)
        antwort_signal = self.audio.listen(5, config.AUTHENTIFIZIERUNG_SAMPLE_RATE, config.RECORD_ANTWORT_TMP_PATH)
        return self.audio.recognize(antwort_signal, config.AUTHENTIFIZIERUNG_SAMPLE_RATE, config.RECORD_ANTWORT_TMP_PATH)
    def start(self):
        benutzer_id = None
        self.audio.text_to_speech("Ja?", config.RECORD_ANTWORT_TMP_PATH)
        signal = self.audio.listen(5, config.AUTHENTIFIZIERUNG_SAMPLE_RATE, config.RECORD_SATZ_TMP_PATH)
        
        if self.predictor_user: # wenn es auth.pth gibt
            name_index, name_label = self.user_authentifizierung(signal)
            pred_id = int(name_label[0][name_index][0])
            pred_name = self.model_user.show_benutzer_name(pred_id)
            pred_noten = name_label[1][name_index][0]

            if pred_noten < config.AUTHENTIFIZIERUNG_MIN_NOTEN or len(name_label[0]) < config.AUTHENTIFIZIERUNG_MIN_KONTO:
                antwort_text = self.dialog("Sind Sie " + pred_name)
                if antwort_text == "ja":
                    benutzer_id = pred_id
            else:
                benutzer_id = pred_id

        if not benutzer_id:
            antwort_text = self.dialog("Wollen Sie ein Konto erstellen?")
            
            if antwort_text == "ja":
                antwort_text = self.dialog("Wie heißt du?")
                if antwort_text:
                    benutzer_id = self.model_user.add_benutzer(antwort_text)
            else:
                self.audio.text_to_speech("Sie müssen ein Konto haben.", config.RECORD_ANTWORT_TMP_PATH)
        
        if benutzer_id:
            self.save_features(signal, benutzer_id)
            input_satz = self.audio.recognize(signal, config.AUTHENTIFIZIERUNG_SAMPLE_RATE, config.RECORD_SATZ_TMP_PATH)
            anmerkung_satz_labels, woerter_anmerkungen, absicht_satz_labels, absicht_class_scores, szenario_satz_labels, szenario_class_scores = self.predictor_text.predict(input_satz)
            pred_absicht_noten = absicht_class_scores[1][absicht_satz_labels]
            pred_szenario_noten = szenario_class_scores[1][szenario_satz_labels]
            if pred_absicht_noten >= config.TEXTKLASSIFIZIERUNG_ABSICHT_MIN_NOTEN and pred_szenario_noten >= config.TEXTKLASSIFIZIERUNG_SZENARIO_MIN_NOTEN:
                output_satz = self.intent_filter(absicht_class_scores[0][absicht_satz_labels], szenario_class_scores[0][szenario_satz_labels], woerter_anmerkungen, anmerkung_satz_labels, benutzer_id)
            else:
                output_satz = "Ich verstehe ihren Absicht nicht"
            self.audio.text_to_speech(output_satz, config.RECORD_SATZ_TMP_PATH)
            if config.AUTHENTIFIZIERUNG_AUTO_TRAINING:
                train_merkmale.train()

engine = Engine()
engine.start()