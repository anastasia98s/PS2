from intends.wetter_intent import WetterIntent
from intends.studienordnung_intent import StudienordnungIntent
from intends.todolist_intent import ToDoListIntent
from intends.wikipedia_intent import WikipediaIntent
from intends.zeit_intent import ZeitIntent
from intends.datum_intent import DatumIntent
from nn_authentifizierung.utils import extract_features
from nn_textklassifizierung.predictor import Predictor as PredictorText
from nn_authentifizierung.predictor import Predictor as PredictorUser
from data.data_controller.model_user import ModelUser
from nn_authentifizierung import train as train_merkmale
import config
from utils.audio import Audio
import os

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
        self.zeit_intent = ZeitIntent()
        self.datum_intent = DatumIntent()
        self.audio = Audio()

    def satz_klassifizieren(self, text):
        return self.predictor_text.predict(text)
    
    def user_authentifizierung(self, signal):
        name_indexs, name_label_scores = self.predictor_user.predict(signal)
        return name_indexs, name_label_scores
    
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
            case (config.SZENARIO_ZEIT, config.ABSICHT_ABFRAGEN): # abfragen
                return self.zeit_intent.abfragen(t_ort)

            ################################### # datum
            case (config.SZENARIO_DATUM, config.ABSICHT_ABFRAGEN): # abfragen
                return self.datum_intent.abfragen(t_datum)

            ################################### # wetter
            case (config.SZENARIO_WETTER, config.ABSICHT_ABFRAGEN): # abfragen
                return self.wetter_intent.abfragen(v_zeit, t_datum, t_ort)

            ################################### # studienordnung
            case (config.SZENARIO_STUDIENORDNUNG, config.ABSICHT_ABFRAGEN): # abfragen
                return self.studienordnung_intent.abfragen(t_thema)

            ################################### # Wikipedia
            case (config.SZENARIO_WIKIPEDIA, config.ABSICHT_ABFRAGEN): # abfragen
                return self.wikipedia_intent.abfragen(t_thema)

            ################################### # todo list
            case (config.SZENARIO_TODO_LIST, config.ABSICHT_ABFRAGEN): # abfragen
                return self.todolist_intent.abfragen(t_artikel, t_zeit, t_datum, user_id)
            case (config.SZENARIO_TODO_LIST, config.ABSICHT_EINGEBEN): # hinzufügen
                
                if not t_datum:
                    t_datum = self.dialog("Kannst du das Datum sagen")
                if not t_zeit:
                    t_zeit = self.dialog("Kannst du die Zeit sagen")

                return self.todolist_intent.eingeben(t_artikel, t_zeit, t_datum, user_id)
            case (config.SZENARIO_TODO_LIST, config.ABSICHT_ENTFERNEN): # löschen
                return self.todolist_intent.entfernen(t_artikel, t_zeit, t_datum, user_id)
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
            
        """ part_length = len(signal) // config.AUDIO_SAVE_SPLIT
    
        for i in range(config.AUDIO_SAVE_SPLIT):
            signal_part = signal[i * part_length : (i + 1) * part_length]
            features = extract_features(signal_part, config.AUTHENTIFIZIERUNG_SAMPLE_RATE)
            self.model_user.add_merkmale(benutzer_id, features) """
            
        """ features = extract_features(signal, config.AUTHENTIFIZIERUNG_SAMPLE_RATE)
        self.model_user.add_merkmale(benutzer_id, features) """
    def dialog(self, satz):
        self.audio.text_to_speech(satz, config.RECORD_ANTWORT_TMP_PATH)
        antwort_signal = self.audio.listen(5, config.AUTHENTIFIZIERUNG_SAMPLE_RATE, config.RECORD_ANTWORT_TMP_PATH)
        return self.audio.recognize(antwort_signal, config.AUTHENTIFIZIERUNG_SAMPLE_RATE, config.RECORD_ANTWORT_TMP_PATH)
    def start(self):
        benutzer_id = None
        signal = self.audio.listen(5, config.AUTHENTIFIZIERUNG_SAMPLE_RATE, config.RECORD_SATZ_TMP_PATH)
        
        if self.predictor_user: # wenn es auth.pth gibt
            name_index, name_label = engine.user_authentifizierung(signal)
            pred_id = int(name_label[0][name_index][0])
            pred_name = self.model_user.show_benutzer_name(pred_id)
            antwort_text = self.dialog("Sind Sie " + pred_name) # wie viel Prozent?
            if antwort_text == "ja":
                benutzer_id = pred_id

        if not benutzer_id:
            antwort_text = self.dialog("Wollen Sie ein Konto eröffnen?")
            
            if antwort_text == "ja":
                antwort_text = self.dialog("Wie heißt du?")
                if antwort_text:
                    benutzer_id = self.model_user.add_benutzer(antwort_text)
            else:
                self.audio.text_to_speech("Sie müssen ein Konto haben.", config.RECORD_ANTWORT_TMP_PATH)
        
        if benutzer_id:
            self.save_features(signal, benutzer_id)
            input_satz = self.audio.recognize(signal, config.AUTHENTIFIZIERUNG_SAMPLE_RATE, config.RECORD_SATZ_TMP_PATH)
            anmerkung_satz_labels, woerter_anmerkungen, absicht_satz_labels, absicht_class_scores, szenario_satz_labels, szenario_class_scores = engine.satz_klassifizieren(input_satz)
            output_satz = self.intent_filter(absicht_class_scores[0][absicht_satz_labels], szenario_class_scores[0][szenario_satz_labels], woerter_anmerkungen, anmerkung_satz_labels, benutzer_id)
            self.audio.text_to_speech(output_satz, config.RECORD_SATZ_TMP_PATH)
            train_merkmale.train()

engine = Engine()
engine.start()