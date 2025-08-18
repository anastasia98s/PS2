import config
import threading
import utils.api
from utils.utils import anmerkungen_inhalt_extrahieren

class EngineProcessor:
    def __init__(self,
                 main_class_engine,
                 speech_to_text,
                 text_to_speech,
                 system_intent):
        
        self.main_class_engine = main_class_engine
        self.speech_to_text = speech_to_text
        self.text_to_speech = text_to_speech
        self.system_intent = system_intent
        self.thread_event = threading.Event()

    def intent_filter(self, absicht, szenario, anmerkungen, anmerkungen_label, user_id):
        if not self.thread_event.is_set():
            t_satz, t_thema, t_aktivitaet, t_zeit, t_datum, t_ort = anmerkungen_inhalt_extrahieren(anmerkungen, anmerkungen_label)

            match (szenario, absicht):
                ################################### # zeit
                case (utils.api.SZENARIO_UHRZEIT, utils.api.ABSICHT_ABFRAGEN): # abfragen
                    intent_result, error_result = utils.api.uhrzeit_intent_abfragen(t_ort)
                    if not error_result:
                        return intent_result
                    else:
                        return "Zeit Intent Error!"

                ################################### # datum
                case (utils.api.SZENARIO_DATUM, utils.api.ABSICHT_ABFRAGEN): # abfragen
                    while True:
                        if not self.thread_event.is_set():
                            intent_result, error_result = utils.api.datum_intent_abfragen(t_datum)
                            if not error_result:
                                return intent_result
                            else:
                                t_datum = self.speech_to_text.intent_variable_error_reask(error_result, status_class_thread=self)
                                if t_datum and any(word in t_datum.lower().split() for word in ["nein", "ne"]):
                                    return "verstehe"
                        else:
                            return None

                ################################### # wetter
                case (utils.api.SZENARIO_WETTER, utils.api.ABSICHT_ABFRAGEN): # abfragen
                    while True:
                        if not self.thread_event.is_set():
                            intent_result, error_result = utils.api.wetter_intent_abfragen(t_zeit, t_datum, t_ort)
                            if not error_result:
                                return intent_result
                            else:
                                if error_result == utils.api.ERROR_VARIABLE_DATUM:
                                    t_datum = self.speech_to_text.intent_variable_error_reask(error_result, status_class_thread=self)
                                    if t_datum and any(word in t_datum.lower().split() for word in ["nein", "ne"]):
                                        return "verstehe"
                                elif error_result == utils.api.ERROR_VARIABLE_ZEIT:
                                    t_zeit = self.speech_to_text.intent_variable_error_reask(error_result, status_class_thread=self)
                                    if t_zeit and any(word in t_zeit.lower().split() for word in ["nein", "ne"]):
                                        return "verstehe"
                                elif error_result == utils.api.ERROR_VARIABLE_ORT:
                                    t_ort = self.speech_to_text.intent_variable_error_reask(error_result, status_class_thread=self)
                                    if t_ort and any(word in t_ort.lower().split() for word in ["nein", "ne"]):
                                        return "verstehe"
                        else:
                            return None

                ################################### # studienordnung
                case (utils.api.SZENARIO_STUDIENORDNUNG, utils.api.ABSICHT_ABFRAGEN): # abfragen
                    self.text_to_speech.text_to_speech("Zum Thema Studienordnung frage ich bei Ollama nach", status_class_thread=self)
                    intent_result, error_result = utils.api.studienordnung_intent_abfragen(t_satz)
                    if not error_result:
                        return intent_result
                    else:
                        return "Studienordnung Intent Error!"

                ################################### # Wikipedia
                case (utils.api.SZENARIO_WIKIPEDIA, utils.api.ABSICHT_ABFRAGEN): # abfragen
                    if t_thema:
                        self.text_to_speech.text_to_speech(f"suche nach {t_thema} in Wikipedia", status_class_thread=self)
                    while True:
                        if not self.thread_event.is_set():
                            intent_result, error_result = utils.api.wikipedia_intent_abfragen(t_satz, t_thema)
                            if not error_result:
                                return intent_result
                            else:
                                if error_result == utils.api.ERROR_VARIABLE_THEMA:
                                    t_thema = self.speech_to_text.intent_variable_error_reask(error_result, status_class_thread=self)
                                    if t_thema and any(word in t_thema.lower().split() for word in ["nein", "ne"]):
                                        return "verstehe"
                        else:
                            return None

                ################################### # todo list
                case (utils.api.SZENARIO_TODO_LIST, utils.api.ABSICHT_ABFRAGEN): # abfragen
                    while True:
                        if not self.thread_event.is_set():
                            intent_result, error_result = utils.api.todolist_intent_abfragen(t_aktivitaet, t_zeit, t_datum, user_id)
                            if not error_result:
                                return intent_result
                            else:
                                if error_result == utils.api.ERROR_VARIABLE_DATUM:
                                    t_datum = self.speech_to_text.intent_variable_error_reask(error_result, status_class_thread=self)
                                    if t_datum and any(word in t_datum.lower().split() for word in ["nein", "ne"]):
                                        return "verstehe"
                                elif error_result == utils.api.ERROR_VARIABLE_ZEIT:
                                    t_zeit = self.speech_to_text.intent_variable_error_reask(error_result, status_class_thread=self)
                                    if t_zeit and any(word in t_zeit.lower().split() for word in ["nein", "ne"]):
                                        return "verstehe"
                        else:
                            return None
                        
                case (utils.api.SZENARIO_TODO_LIST, utils.api.ABSICHT_EINGEBEN): # hinzufügen
                    """ if not t_datum:
                        t_datum = self.speech_to_text.intent_variable_error_reask(1, neue_daten_abfragen=True, status_class_thread=self)
                        if t_datum and any(word in t_datum.lower().split() for word in ["nein", "ne"]):
                            return "verstehe"
                    if not t_zeit:
                        t_zeit = self.speech_to_text.intent_variable_error_reask(2, neue_daten_abfragen=True, status_class_thread=self)
                        if t_zeit and any(word in t_zeit.lower().split() for word in ["nein", "ne"]):
                            return "verstehe" """

                    while True:
                        if not self.thread_event.is_set():
                            intent_result, error_result = utils.api.todolist_intent_eingeben(t_aktivitaet, t_zeit, t_datum, user_id)
                            if not error_result:
                                return intent_result
                            else:
                                if error_result == utils.api.ERROR_VARIABLE_DATUM:
                                    t_datum = self.speech_to_text.intent_variable_error_reask(error_result, status_class_thread=self)
                                    if t_datum and any(word in t_datum.lower().split() for word in ["nein", "ne"]):
                                        return "verstehe"
                                elif error_result == utils.api.ERROR_VARIABLE_ZEIT:
                                    t_zeit = self.speech_to_text.intent_variable_error_reask(error_result, status_class_thread=self)
                                    if t_zeit and any(word in t_zeit.lower().split() for word in ["nein", "ne"]):
                                        return "verstehe"
                                elif error_result == utils.api.ERROR_VARIABLE_AKTIVITAET:
                                    t_aktivitaet = self.speech_to_text.intent_variable_error_reask(error_result, status_class_thread=self)
                                    if t_aktivitaet and any(word in t_aktivitaet.lower().split() for word in ["nein", "ne"]):
                                        return "verstehe"
                        else:
                            return None

                case (utils.api.SZENARIO_TODO_LIST, utils.api.ABSICHT_ENTFERNEN): # löschen
                    while True:
                        if not self.thread_event.is_set():
                            intent_result, error_result = utils.api.todolist_intent_entfernen(t_aktivitaet, t_zeit, t_datum, user_id)
                            if not error_result:
                                return intent_result
                            else:
                                if error_result == utils.api.ERROR_VARIABLE_DATUM:
                                    t_datum = self.speech_to_text.intent_variable_error_reask(error_result, status_class_thread=self)
                                    if t_datum and any(word in t_datum.lower().split() for word in ["nein", "ne"]):
                                        return "verstehe"
                                elif error_result == utils.api.ERROR_VARIABLE_ZEIT:
                                    t_zeit = self.speech_to_text.intent_variable_error_reask(error_result, status_class_thread=self)
                                    if t_zeit and any(word in t_zeit.lower().split() for word in ["nein", "ne"]):
                                        return "verstehe"
                                elif error_result == utils.api.ERROR_VARIABLE_AKTIVITAET:
                                    t_aktivitaet = self.speech_to_text.intent_variable_error_reask(error_result, status_class_thread=self)
                                    if t_aktivitaet and any(word in t_aktivitaet.lower().split() for word in ["nein", "ne"]):
                                        return "verstehe"
                        else:
                            return None
                        
                ################################### # System
                case (utils.api.SZENARIO_SYSTEM, utils.api.ABSICHT_ZURUECKGEHEN):
                    intent_result, error_result = self.system_intent.zurueckgehen()
                    if not error_result:
                        return intent_result
                    else:
                        return "System Intent Error!"
                    
                case (utils.api.SZENARIO_SYSTEM, utils.api.ABSICHT_WEITERGEHEN):
                    intent_result, error_result = self.system_intent.weitergehen()
                    if not error_result:
                        return intent_result
                    else:
                        return "System Intent Error!"
                    
                case (utils.api.SZENARIO_SYSTEM, utils.api.ABSICHT_WIEDERHOLEN):
                    intent_result, error_result = self.system_intent.wiederholen()
                    if not error_result:
                        return intent_result
                    else:
                        return "System Intent Error!"
                    
                case (utils.api.SZENARIO_SYSTEM, utils.api.ABSICHT_ABBRECHEN):
                    intent_result, error_result = self.system_intent.abbrechen()
                    if not error_result:
                        return intent_result
                    else:
                        return "System Intent Error!"
                    
                ################################### # Youtube
                case (utils.api.SZENARIO_YOUTUBE, utils.api.ABSICHT_ABFRAGEN): # abfragen
                    if t_thema:
                        self.text_to_speech.text_to_speech(f"suche nach {t_thema} in YouTube", status_class_thread=self)
                    while True:
                        if not self.thread_event.is_set():
                            intent_result, error_result, error_request = utils.api.youtube_intent_abfragen(t_thema)
                            if not error_result:
                                if not error_request:
                                    self.system_intent.playlist = intent_result
                                    self.system_intent.playlist_index = 0
                                    system_intent_result, _ = self.system_intent.website_oeffnen()
                                    return system_intent_result
                                else:
                                    return intent_result
                            else:
                                if error_result == utils.api.ERROR_VARIABLE_THEMA:
                                    t_thema = self.speech_to_text.intent_variable_error_reask(error_result, status_class_thread=self)
                                    if t_thema and any(word in t_thema.lower().split() for word in ["nein", "ne"]):
                                        return "verstehe"
                        else:
                            return None
                                            
                ################################### # Search Engine
                case (utils.api.SZENARIO_SEARCH_ENGINE, utils.api.ABSICHT_ABFRAGEN): # abfragen
                    if t_thema:
                        self.text_to_speech.text_to_speech(f"suche nach {t_thema} in Google", status_class_thread=self)
                    while True:
                        if not self.thread_event.is_set():
                            intent_result, error_result, error_request = utils.api.search_engine_intent_abfragen(t_thema)
                            if not error_result:
                                if not error_request:
                                    self.system_intent.playlist = intent_result
                                    self.system_intent.playlist_index = 0
                                    system_intent_result, _ = self.system_intent.website_oeffnen()
                                    return system_intent_result
                                else:
                                    return intent_result
                            else:
                                if error_result == utils.api.ERROR_VARIABLE_THEMA:
                                    t_thema = self.speech_to_text.intent_variable_error_reask(error_result, status_class_thread=self)
                                    if t_thema and any(word in t_thema.lower().split() for word in ["nein", "ne"]):
                                        return "verstehe"
                        else:
                            return None
                case _:
                    return "Ich verstehe ihren Absicht nicht!"
        else:
            return None
            
    def start(self, wake_word_signal):
        if not self.thread_event.is_set():


            id_auth_result, error_request = self.main_class_engine.authentifizieren(wake_word_signal, status_class_thread=self) #antwort_signal_trim
            if not error_request:
                self.main_class_engine.benutzer_id = id_auth_result
                if self.main_class_engine.benutzer_id:
                    self.text_to_speech.text_to_speech("Ja?", status_class_thread=self)
                    antwort_signal_trim, antwort_text = self.speech_to_text.listen_recognize(3, utils.api.AUDIO_SAMPLE_RATE, status_class_thread=self, loading_speech=True if self.main_class_engine.benutzer_id else False)
                    # -------------------------------------------------------------------------------------------------

                    textklassifizierung_data, error_request = utils.api.predictor_text_predict(antwort_text)

                    if not error_request:
                        anmerkung_satz_labels = textklassifizierung_data["anmerkung_satz_labels"]
                        woerter_anmerkungen = textklassifizierung_data["woerter_anmerkungen"]
                        absicht_satz_labels = textklassifizierung_data["absicht_satz_labels"]
                        absicht_class_scores = textklassifizierung_data["absicht_class_scores"]
                        szenario_satz_labels = textklassifizierung_data["szenario_satz_labels"]
                        szenario_class_scores = textklassifizierung_data["szenario_class_scores"]
                        
                        pred_absicht_noten = absicht_class_scores[1][absicht_satz_labels]
                        pred_szenario_noten = szenario_class_scores[1][szenario_satz_labels]
                        print("Absichtswahrscheinlichkeit: " + str(pred_absicht_noten) + "/" + str(config.TEXTKLASSIFIZIERUNG_ABSICHT_MIN_NOTEN))
                        print("Szenarioswahrscheinlichkeit: " + str(pred_szenario_noten) + "/" + str(config.TEXTKLASSIFIZIERUNG_SZENARIO_MIN_NOTEN))
                        if pred_absicht_noten >= config.TEXTKLASSIFIZIERUNG_ABSICHT_MIN_NOTEN and pred_szenario_noten >= config.TEXTKLASSIFIZIERUNG_SZENARIO_MIN_NOTEN:
                            output_satz = self.intent_filter(absicht_class_scores[0][absicht_satz_labels], szenario_class_scores[0][szenario_satz_labels], woerter_anmerkungen, anmerkung_satz_labels, self.main_class_engine.benutzer_id)
                        else:
                            output_satz = "Ich bin für diese Absicht noch nicht trainiert!"
                    else:
                        output_satz = textklassifizierung_data

                    self.text_to_speech.text_to_speech(output_satz, status_class_thread=self)

                    # ------------------------------------------------------------------------------------------------
                    save_features_result, error_request = utils.api.save_features(wake_word_signal, self.main_class_engine.benutzer_id) #antwort_signal_trim
                    if error_request:
                        print(save_features_result)
                    
                    """ if config.AUTHENTIFIZIERUNG_AUTO_TRAINING:
                        train_auth_ki_result, error_request = utils.api.train_authentifizierung_ki()
                        if error_request:
                            print(train_auth_ki_result) """
                else:
                    self.text_to_speech.text_to_speech("Sie müssen ein Konto haben.", status_class_thread=self)
            else:
                self.text_to_speech.text_to_speech(id_auth_result, status_class_thread=self)

        self.main_class_engine.finished_run_engine_processor(self)