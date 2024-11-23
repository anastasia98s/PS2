from neural_network.nn_authentifizierung.predictor import Predictor as PredictorUser
from utils.data_controller.user_controller.presenter import PresenterUser
from neural_network.nn_authentifizierung import train as train_merkmale
import config
import os
import warnings
import threading
from utils.audio.aktivierungswort import Aktivierungswort
from utils.audio.speech_to_text import SpeechToText
from utils.audio.text_to_speech import TextToSpeech
from utils.engine.processor import EngineProcessor
from intents.wetter_intent import WetterIntent
from intents.studienordnung.studienordnung_intent import StudienordnungIntent
from intents.todolist_intent import ToDoListIntent
from intents.wikipedia_intent import WikipediaIntent
from intents.uhrzeit_intent import UhrzeitIntent
from intents.datum_intent import DatumIntent
from intents.system_intent import SystemIntent
from intents.youtube_intent import YoutubeIntent
from intents.search_engine_intent import SearchEngineIntent
warnings.filterwarnings("ignore")

class Engine:
    def __init__(self):
        self.presenter_user = PresenterUser()
        self.aktivierungswort = Aktivierungswort()
        self.text_to_speech = TextToSpeech()
        self.speech_to_text = SpeechToText(self.text_to_speech)
        self.wetter_intent = WetterIntent(self.text_to_speech)
        self.studienordnung_intent = StudienordnungIntent(self.text_to_speech)
        self.todolist_intent = ToDoListIntent()
        self.wikipedia_intent = WikipediaIntent(self.text_to_speech)
        self.uhrzeit_intent = UhrzeitIntent()
        self.datum_intent = DatumIntent()
        self.system_intent = SystemIntent()
        self.youtube_intent = YoutubeIntent(self.system_intent, self.text_to_speech)
        self.search_engine_intent = SearchEngineIntent(self.system_intent, self.text_to_speech)
        self.benutzer_id = None
        self.run_engine_processor = []
        if os.path.exists(config.AUTHENTIFIZIERUNG_TRAINED_PATH):
            self.predictor_user = PredictorUser(config.AUTHENTIFIZIERUNG_TRAINED_PATH)
        else:
            self.predictor_user = None
    
    def authentifizieren(self, signal):
        if self.predictor_user and self.benutzer_id is None: # wenn es auth.pth gibt
            name_index, name_label = self.predictor_user.predict(signal)
            pred_id = int(name_label[0][name_index][0])
            pred_name = self.presenter_user.show_benutzer_name(pred_id)
            pred_noten = name_label[1][name_index][0]

            if pred_noten < config.AUTHENTIFIZIERUNG_MIN_NOTEN or len(name_label[0]) < config.AUTHENTIFIZIERUNG_MIN_KONTO:
                antwort_text = self.speech_to_text.dialog(0.5, "Sind Sie " + pred_name)
                if any(word in antwort_text.lower().split() for word in ["ja", "genau"]):
                    self.benutzer_id = pred_id
                else:
                    antwort_text = self.speech_to_text.dialog(0.5, "Haben Sie bereits ein Konto?")
                    if any(word in antwort_text.lower().split() for word in ["ja", "genau"]):
                        for label in name_label[0]:
                            geg_id = int(label)
                            geg_name = self.presenter_user.show_benutzer_name(geg_id)
                            antwort_text = self.speech_to_text.dialog(0.5, "Sind Sie " + geg_name)
                            if any(word in antwort_text.lower().split() for word in ["ja", "genau"]):
                                self.benutzer_id = geg_id
                                break
            else:
                self.benutzer_id = pred_id

        if not self.benutzer_id:
            antwort_text = self.speech_to_text.dialog(0.5, "Wollen Sie ein Konto erstellen?")
            
            if any(word in antwort_text.lower().split() for word in ["ja", "okay"]):
                antwort_text = self.speech_to_text.dialog(0.5, "Wie heißt du?")
                if antwort_text:
                    self.benutzer_id = self.presenter_user.add_benutzer(antwort_text)
    
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
            self.aktivierungswort.wake_word_recognize(config.AUDIO_SAMPLE_RATE)
            self.shutdown_run_engine_processor()
            self.text_to_speech.text_to_speech("Ja?")
            antwort_signal_trim, antwort_text = self.speech_to_text.listen_recognize(3, config.AUDIO_SAMPLE_RATE)
            
            self.authentifizieren(antwort_signal_trim)
            if self.benutzer_id:
                self.presenter_user.save_features(antwort_signal_trim, self.benutzer_id)
                engine_processor = EngineProcessor(self.speech_to_text,
                                                   self.text_to_speech,
                                                   self,
                                                   self.wetter_intent,
                                                   self.studienordnung_intent,
                                                   self.todolist_intent,
                                                   self.wikipedia_intent,
                                                   self.uhrzeit_intent,
                                                   self.datum_intent,
                                                   self.system_intent,
                                                   self.youtube_intent,
                                                   self.search_engine_intent)
                self.run_engine_processor.append(engine_processor)
                main_thread = threading.Thread(target=engine_processor.start, args=(self.benutzer_id, antwort_text))
                main_thread.start()
                
                if config.AUTHENTIFIZIERUNG_AUTO_TRAINING:
                    train_merkmale.train()
            else:
                self.text_to_speech.text_to_speech("Sie müssen ein Konto haben.")

if __name__ == "__main__":
    engine = Engine()
    engine.start()