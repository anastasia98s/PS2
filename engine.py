from intends.wetter_intent import WetterIntent
from intends.studienordnung_intent import StudienordnungIntent
from intends.todolist_intent import ToDoListIntent
from intends.wikipedia_intent import WikipediaIntent
from intends.zeit_intent import ZeitIntent
from intends.datum_intent import DatumIntent

from nn_textklassifizierung.predictor import Predictor as PredictorText
from nn_authentifizierung.predictor import Predictor as PredictorUser
import config
from utils.audio import Audio

class Engine:
    def __init__(self):
        self.predictor_text = PredictorText(config.TEXTKLASSIFIZIERUNG_TRAINED_PATH)
        self.predictor_user = PredictorUser(config.AUTHENTIFIZIERUNG_TRAINED_PATH)
        self.wetter_intent = WetterIntent()
        self.studienordnung_intent = StudienordnungIntent()
        self.todolist_intent = ToDoListIntent()
        self.wikipedia_intent = WikipediaIntent()
        self.zeit_intent = ZeitIntent()
        self.datum_intent = DatumIntent()
        self.audio = Audio()

    def satz_klassifizieren(self, text):
        return self.predictor_text.predict(text)

    def user_speech_recognition(self):
        signal = self.audio.listen(5, config.AUTHENTIFIZIERUNG_SAMPLE_RATE)
        text = self.audio.recognize(signal, config.AUTHENTIFIZIERUNG_SAMPLE_RATE)
        name_indexs, name_label_scores = self.predictor_user.predict(signal)
        return text, name_indexs, name_label_scores
    
    def intent_filter(self, absicht, szenario, anmerkungen, anmerkungen_label, user_id):
        v_thema = []
        v_artikel = []
        v_zeit = []
        v_datum = []
        v_ort = []
        v_zustand = []
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
                case config.ANMERKUNG_ZUSTAND: # zustand
                    v_zustand.append(anmerkungen[1][index])

        t_thema = " ".join(v_thema)
        t_artikel = " ".join(v_artikel)
        t_zeit = " ".join(v_zeit)
        t_datum = " ".join(v_datum)
        t_ort = " ".join(v_ort)
        t_zustand = " ".join(v_zustand)

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
                return self.todolist_intent.eingeben(t_artikel, t_zeit, t_datum, user_id)
            case (config.SZENARIO_TODO_LIST, config.ABSICHT_AENDERN): # ändern
                return self.todolist_intent.aendern(t_artikel, t_zeit, t_datum, t_zustand, user_id)
            case (config.SZENARIO_TODO_LIST, config.ABSICHT_ENTFERNEN): # löschen
                return self.todolist_intent.entfernen(t_artikel, t_zeit, t_datum, user_id)
            case _:
                return "Unknown scenario or absicht"

    def start(self):
        text, name_index, name_label = engine.user_speech_recognition()
        print("User: " + name_label[0][name_index][0])
        anmerkung_satz_labels, woerter_anmerkungen, absicht_satz_labels, absicht_class_scores, szenario_satz_labels, szenario_class_scores = engine.satz_klassifizieren(text)
        antwort_satz = self.intent_filter(absicht_class_scores[0][absicht_satz_labels], szenario_class_scores[0][szenario_satz_labels], woerter_anmerkungen, anmerkung_satz_labels, name_label[0][name_index][0])
        self.audio.text_to_speech(antwort_satz)

engine = Engine()
engine.start()