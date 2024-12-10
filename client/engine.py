import warnings
import threading
from utils.audio.aktivierungswort import Aktivierungswort
from utils.audio.speech_to_text import SpeechToText
from utils.audio.text_to_speech import TextToSpeech
from utils.engine.processor import EngineProcessor
from utils.engine.system_intent import SystemIntent
import utils.api
warnings.filterwarnings("ignore")

class Engine:
    def __init__(self):
        self.aktivierungswort = Aktivierungswort()
        self.text_to_speech = TextToSpeech()
        self.speech_to_text = SpeechToText(self.text_to_speech)
        self.system_intent = SystemIntent()
        self.benutzer_id = None
        self.run_engine_processor = []
    
    def authentifizieren(self, signal):
        if not self.benutzer_id:
            auth_data, error_request = utils.api.authentifizierung(signal)
            if error_request:
                return auth_data, 1
            pred_id = auth_data["pred_id"]
            name_label = auth_data["name_label"]

            if pred_id:
                pred_name, error_request = utils.api.show_benutzer_name(pred_id)
                if error_request:
                    return pred_name, 1
                antwort_text = self.speech_to_text.dialog(0.5, "Sind Sie " + pred_name)
                if any(word in antwort_text.lower().split() for word in ["ja", "genau"]):
                    return pred_id, None
            
            if isinstance(name_label, list) and len(name_label) > 0 and len(name_label[0]) > 1:
                antwort_text = self.speech_to_text.dialog(0.5, "Haben Sie bereits ein Konto?")
                if any(word in antwort_text.lower().split() for word in ["ja", "genau"]):
                    for label in name_label[0]:
                        geg_id = int(label)
                        if pred_id:
                            if geg_id == pred_id:
                                continue
                        geg_name, error_request = utils.api.show_benutzer_name(geg_id)
                        if error_request:
                            return geg_name, 1
                        antwort_text = self.speech_to_text.dialog(0.5, "Sind Sie " + geg_name)
                        if any(word in antwort_text.lower().split() for word in ["ja", "genau"]):
                            return geg_id, None

            antwort_text = self.speech_to_text.dialog(0.5, "Wollen Sie ein Konto erstellen?")
            if any(word in antwort_text.lower().split() for word in ["ja", "okay"]):
                antwort_text = self.speech_to_text.dialog(0.5, "Wie heißt du?")
                if antwort_text:
                    neues_id, error_request = utils.api.add_benutzer(antwort_text)
                    if error_request:
                        return neues_id, 1
                    return neues_id, None
            else:
                return None, None
        else:
            return self.benutzer_id, None
    
    def shutdown_run_engine_processor(self):
        if len(self.run_engine_processor) > 0:
            for engine_processor in self.run_engine_processor:
                engine_processor.thread_event.set()
                #self.run_engine_processor.remove(engine_processor)

    def finished_run_engine_processor(self, engine_processor):
        #print(len(self.run_engine_processor), engine_processor)
        self.run_engine_processor.remove(engine_processor)
        #print(len(self.run_engine_processor))

    def start(self):
        self.text_to_speech.text_to_speech("Ich bin bereit")
        while True:
            wake_word_signal = self.aktivierungswort.wake_word_recognize(utils.api.AUDIO_SAMPLE_RATE)
            self.shutdown_run_engine_processor()
            self.text_to_speech.text_to_speech("Ja?")
            antwort_signal_trim, antwort_text = self.speech_to_text.listen_recognize(3, utils.api.AUDIO_SAMPLE_RATE, loading_speech=True if self.benutzer_id else False)
            id_auth_result, error_request = self.authentifizieren(wake_word_signal) #antwort_signal_trim
            if not error_request:
                self.benutzer_id = id_auth_result
                if self.benutzer_id:
                    engine_processor = EngineProcessor(self,
                                                    self.speech_to_text,
                                                    self.text_to_speech,
                                                    self.system_intent)
                    self.run_engine_processor.append(engine_processor)
                    main_thread = threading.Thread(target=engine_processor.start, args=(self.benutzer_id, antwort_text))
                    main_thread.start()

                    save_features_result, error_request = utils.api.save_features(wake_word_signal, self.benutzer_id) #antwort_signal_trim
                    if error_request:
                        print(save_features_result)
                    
                    """ if config.AUTHENTIFIZIERUNG_AUTO_TRAINING:
                        train_auth_ki_result, error_request = utils.api.train_authentifizierung_ki()
                        if error_request:
                            print(train_auth_ki_result) """
                else:
                    self.text_to_speech.text_to_speech("Sie müssen ein Konto haben.")
            else:
                self.text_to_speech.text_to_speech(id_auth_result)

if __name__ == "__main__":
    engine = Engine()
    engine.start()