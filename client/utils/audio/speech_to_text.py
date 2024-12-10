import config
import re
import utils.audio.utils
import threading
import utils.api

class SpeechToText:
    def __init__(self, text_to_speech):
        self.lock = threading.Lock()
        self.text_to_speech = text_to_speech

    def recognize(self, signal, status_class_thread=None):
        with self.lock:
            if status_class_thread and status_class_thread.thread_event.is_set():
                return None
            
            return utils.api.speech_to_text_recognize(signal)
                
    def listen_recognize(self, silence_duration, sample_rate, status_class_thread=None, loading_speech=False):
        while True:
            if status_class_thread and status_class_thread.thread_event.is_set():
                return None, None
            
            antwort_signal, antwort_signal_trim = utils.audio.utils.listen(silence_duration, sample_rate, status_class_thread=status_class_thread)
            if loading_speech:
                self.text_to_speech.text_to_speech("einen Moment", status_class_thread=status_class_thread)
            antwort_text, error_request = self.recognize(antwort_signal, status_class_thread=status_class_thread)
            
            if error_request:
                self.text_to_speech.text_to_speech("Error, nochmal bitte", status_class_thread=status_class_thread)
            elif not antwort_text:
                self.text_to_speech.text_to_speech("nochmal bitte", status_class_thread=status_class_thread)
            else:
                antwort_text = re.sub(r'[.!?]$', '', antwort_text)
                print("Sie haben gesagt: " + antwort_text)
                break
        
        return antwort_signal_trim, antwort_text
    
    def dialog(self, silence_duration, satz, status_class_thread=None):
        if status_class_thread and status_class_thread.thread_event.is_set():
            return None
        
        self.text_to_speech.text_to_speech(satz, status_class_thread=status_class_thread) # self.audio.text_to_speech(satz)
        _, antwort_text = self.listen_recognize(silence_duration, utils.api.AUDIO_SAMPLE_RATE, status_class_thread=status_class_thread)
        
        return antwort_text
    
    def intent_variable_error_reask(self, errortyp, neue_daten_abfragen=False, status_class_thread=None):
        if status_class_thread and status_class_thread.thread_event.is_set():
                return None
        
        wd_text = "nochmal " if not neue_daten_abfragen else ""
        
        variable_typen = {
            utils.api.ERROR_VARIABLE_DATUM: "das Datum",
            utils.api.ERROR_VARIABLE_ZEIT: "die Zeit",
            utils.api.ERROR_VARIABLE_ORT: "der Ort",
            utils.api.ERROR_VARIABLE_AKTIVITAET: "den Terminnamen oder die Aktivität",
            utils.api.ERROR_VARIABLE_THEMA: "das Thema"
        }

        variable_name = variable_typen.get(errortyp)
        if not variable_name:
            self.text_to_speech.text_to_speech("Es gab ein Problem mit dem System. Bitte versuche es erneut.", status_class_thread=status_class_thread)
            # sys.exit("Das Programm wird beendet.")
        return self.dialog(1, f"Kannst du {variable_name} {wd_text}sagen?", status_class_thread=status_class_thread)