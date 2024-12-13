import re
import utils.audio.utils
import threading
import utils.api
from utils.utils import reask_text

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
        
        result_reask, error_variable = reask_text(errortyp, neue_daten_abfragen)
        
        if error_variable:
            self.text_to_speech.text_to_speech(result_reask, status_class_thread=status_class_thread)
            
        return self.dialog(1, result_reask, status_class_thread=status_class_thread)