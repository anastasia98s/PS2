import numpy as np
import config
import whisper
import re
import speech_recognition as sr
import utils.audio.utils

class STT:
    def __init__(self, text_to_speech):
        self.text_to_speech = text_to_speech
        if config.LEICHTES_ASR_MODELL:
            self.recognizer = sr.Recognizer()
        else:
            self.recognizer = whisper.load_model(config.SPEECH_RECOGNITION_MODELL, config.DEVICE)

    def recognize(self, signal):
        if config.LEICHTES_ASR_MODELL:
            with sr.AudioFile(config.RECORD_TMP_PATH) as source:
                audio_data = self.recognizer.record(source)
                try:
                    text = self.recognizer.recognize_google(audio_data, language=config.AUDIO_SPRACHE)
                    return text
                except sr.UnknownValueError:
                    print("Entschuldigung, ich konnte die Audioaufnahme nicht verstehen.")
                    return None
                except sr.RequestError as e:
                    print("Konnte keine Ergebnisse anfordern; {0}".format(e))
                    return None
        else:
            signal = signal.astype(np.float32)
            signal = whisper.pad_or_trim(signal)
            result = self.recognizer.transcribe(signal, language=config.WHISPER_SPRACHE)
            sr_text = result["text"]
            if sr_text:
                no_speech_prob = result['segments'][0]['no_speech_prob']
                if no_speech_prob < config.NO_SPEECH_MAX_NOTEN:
                    return sr_text.strip()
                else:
                    return None
            else:
                return None
                
    def listen_recognize(self, silence_duration, sample_rate):
        while True:
            antwort_signal, antwort_signal_trim = utils.audio.utils.listen(silence_duration, sample_rate)
            antwort_text = self.recognize(antwort_signal)
            
            if not antwort_text:
                self.text_to_speech.text_to_speech("nochmal bitte")
            else:
                antwort_text = re.sub(r'[.!?]$', '', antwort_text)
                print("Sie haben gesagt: " + antwort_text)
                break

        return antwort_signal_trim, antwort_text
    
    def dialog(self, silence_duration, satz):
        self.text_to_speech.text_to_speech(satz) # self.audio.text_to_speech(satz)
        _, antwort_text = self.listen_recognize(silence_duration, config.AUDIO_SAMPLE_RATE)
        return antwort_text
    
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
            self.text_to_speech.text_to_speech("Es gab ein Problem mit dem System. Bitte versuche es erneut.")
            # sys.exit("Das Programm wird beendet.")
        return self.dialog(1, f"Kannst du {variable_name} {wd_text}sagen?")