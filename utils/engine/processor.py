import config
from intents.wetter_intent import WetterIntent
from intents.studienordnung.studienordnung_intent import StudienordnungIntent
from intents.todolist_intent import ToDoListIntent
from intents.wikipedia_intent import WikipediaIntent
from intents.uhrzeit_intent import UhrzeitIntent
from intents.datum_intent import DatumIntent
from neural_network.nn_textklassifizierung.predictor import Predictor as PredictorText
import threading

class EngineProcessor:
    def __init__(self, speech_to_text, text_to_speech, main_class_engine):
        self.predictor_text = PredictorText(config.TEXTKLASSIFIZIERUNG_TRAINED_PATH)
        self.wetter_intent = WetterIntent(self)
        self.studienordnung_intent = StudienordnungIntent(self)
        self.todolist_intent = ToDoListIntent(self)
        self.wikipedia_intent = WikipediaIntent(self)
        self.uhrzeit_intent = UhrzeitIntent(self)
        self.datum_intent = DatumIntent(self)
        self.speech_to_text = speech_to_text
        self.text_to_speech = text_to_speech
        self.main_class_engine = main_class_engine
        self.thread_event = threading.Event()

    def intent_filter(self, absicht, szenario, anmerkungen, anmerkungen_label, user_id):
        if not self.thread_event.is_set():
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
                        if not self.thread_event.is_set():
                            intent_result, error_result = self.datum_intent.abfragen(t_datum)
                            if not error_result:
                                return intent_result
                            else:
                                t_datum = self.speech_to_text.intent_variable_error_reask(error_result, status_class_thread=self)
                                if t_datum and any(word in t_datum.lower().split() for word in ["nein", "ne"]):
                                    return "verstehe"
                        else:
                            return None

                ################################### # wetter
                case (config.SZENARIO_WETTER, config.ABSICHT_ABFRAGEN): # abfragen
                    while True:
                        if not self.thread_event.is_set():
                            intent_result, error_result = self.wetter_intent.abfragen(t_zeit, t_datum, t_ort)
                            if not error_result:
                                return intent_result
                            else:
                                if error_result == config.ERROR_VARIABLE_DATUM:
                                    t_datum = self.speech_to_text.intent_variable_error_reask(error_result, status_class_thread=self)
                                    if t_datum and any(word in t_datum.lower().split() for word in ["nein", "ne"]):
                                        return "verstehe"
                                elif error_result == config.ERROR_VARIABLE_ZEIT:
                                    t_zeit = self.speech_to_text.intent_variable_error_reask(error_result, status_class_thread=self)
                                    if t_zeit and any(word in t_zeit.lower().split() for word in ["nein", "ne"]):
                                        return "verstehe"
                                elif error_result == config.ERROR_VARIABLE_ORT:
                                    t_ort = self.speech_to_text.intent_variable_error_reask(error_result, status_class_thread=self)
                                    if t_ort and any(word in t_ort.lower().split() for word in ["nein", "ne"]):
                                        return "verstehe"
                        else:
                            return None

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
                        if not self.thread_event.is_set():
                            intent_result, error_result = self.todolist_intent.abfragen(t_aktivitaet, t_zeit, t_datum, user_id)
                            if not error_result:
                                return intent_result
                            else:
                                if error_result == config.ERROR_VARIABLE_DATUM:
                                    t_datum = self.speech_to_text.intent_variable_error_reask(error_result, status_class_thread=self)
                                    if t_datum and any(word in t_datum.lower().split() for word in ["nein", "ne"]):
                                        return "verstehe"
                                elif error_result == config.ERROR_VARIABLE_ZEIT:
                                    t_zeit = self.speech_to_text.intent_variable_error_reask(error_result, status_class_thread=self)
                                    if t_zeit and any(word in t_zeit.lower().split() for word in ["nein", "ne"]):
                                        return "verstehe"
                        else:
                            return None
                case (config.SZENARIO_TODO_LIST, config.ABSICHT_EINGEBEN): # hinzufügen
                    
                    if not t_datum:
                        t_datum = self.speech_to_text.intent_variable_error_reask(1, neue_daten_abfragen=True, status_class_thread=self)
                        if t_datum and any(word in t_datum.lower().split() for word in ["nein", "ne"]):
                            return "verstehe"
                    if not t_zeit:
                        t_zeit = self.speech_to_text.intent_variable_error_reask(2, neue_daten_abfragen=True, status_class_thread=self)
                        if t_zeit and any(word in t_zeit.lower().split() for word in ["nein", "ne"]):
                            return "verstehe"

                    while True:
                        if not self.thread_event.is_set():
                            intent_result, error_result = self.todolist_intent.eingeben(t_aktivitaet, t_zeit, t_datum, user_id)
                        
                            if not error_result:
                                return intent_result
                            else:
                                if error_result == config.ERROR_VARIABLE_DATUM:
                                    t_datum = self.speech_to_text.intent_variable_error_reask(error_result, status_class_thread=self)
                                    if t_datum and any(word in t_datum.lower().split() for word in ["nein", "ne"]):
                                        return "verstehe"
                                elif error_result == config.ERROR_VARIABLE_ZEIT:
                                    t_zeit = self.speech_to_text.intent_variable_error_reask(error_result, status_class_thread=self)
                                    if t_zeit and any(word in t_zeit.lower().split() for word in ["nein", "ne"]):
                                        return "verstehe"
                                elif error_result == config.ERROR_VARIABLE_AKTIVITAET:
                                    t_aktivitaet = self.speech_to_text.intent_variable_error_reask(error_result, status_class_thread=self)
                                    if t_aktivitaet and any(word in t_aktivitaet.lower().split() for word in ["nein", "ne"]):
                                        return "verstehe"
                        else:
                            return None

                case (config.SZENARIO_TODO_LIST, config.ABSICHT_ENTFERNEN): # löschen
                    while True:
                        if not self.thread_event.is_set():
                            intent_result, error_result = self.todolist_intent.entfernen(t_aktivitaet, t_zeit, t_datum, user_id)
                            if not error_result:
                                return intent_result
                            else:
                                if error_result == config.ERROR_VARIABLE_DATUM:
                                    t_datum = self.speech_to_text.intent_variable_error_reask(error_result, status_class_thread=self)
                                    if t_datum and any(word in t_datum.lower().split() for word in ["nein", "ne"]):
                                        return "verstehe"
                                elif error_result == config.ERROR_VARIABLE_ZEIT:
                                    t_zeit = self.speech_to_text.intent_variable_error_reask(error_result, status_class_thread=self)
                                    if t_zeit and any(word in t_zeit.lower().split() for word in ["nein", "ne"]):
                                        return "verstehe"
                                elif error_result == config.ERROR_VARIABLE_AKTIVITAET:
                                    t_aktivitaet = self.speech_to_text.intent_variable_error_reask(error_result, status_class_thread=self)
                                    if t_aktivitaet and any(word in t_aktivitaet.lower().split() for word in ["nein", "ne"]):
                                        return "verstehe"
                        else:
                            return None
                case _:
                    return "Ich verstehe dich nicht."
        else:
            return None
            
    def start(self, benutzer_id, antwort_text):
        if not self.thread_event.is_set():
            anmerkung_satz_labels, woerter_anmerkungen, absicht_satz_labels, absicht_class_scores, szenario_satz_labels, szenario_class_scores = self.predictor_text.predict(antwort_text)
            pred_absicht_noten = absicht_class_scores[1][absicht_satz_labels]
            pred_szenario_noten = szenario_class_scores[1][szenario_satz_labels]
            print("Absichtswahrscheinlichkeit: " + str(pred_absicht_noten) + "/" + str(config.TEXTKLASSIFIZIERUNG_ABSICHT_MIN_NOTEN))
            print("Szenarioswahrscheinlichkeit: " + str(pred_szenario_noten) + "/" + str(config.TEXTKLASSIFIZIERUNG_SZENARIO_MIN_NOTEN))
            if pred_absicht_noten >= config.TEXTKLASSIFIZIERUNG_ABSICHT_MIN_NOTEN and pred_szenario_noten >= config.TEXTKLASSIFIZIERUNG_SZENARIO_MIN_NOTEN:
                output_satz = self.intent_filter(absicht_class_scores[0][absicht_satz_labels], szenario_class_scores[0][szenario_satz_labels], woerter_anmerkungen, anmerkung_satz_labels, benutzer_id)
            else:
                output_satz = "Ich verstehe ihren Absicht nicht"

            self.text_to_speech.text_to_speech(output_satz, status_class_thread=self)

        self.main_class_engine.finished_run_engine_processor(self)