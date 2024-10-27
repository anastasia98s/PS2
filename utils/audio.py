import speech_recognition as sr
import sounddevice as sd
import wave
import numpy as np
from gtts import gTTS
#import pyttsx3
import os
import config

class Audio:
    def __init__(self, language="de-DE"):
        self.recognizer = sr.Recognizer()
        self.language = language
        #self.pyttsx3 = pyttsx3.init()
        #self.set_sprache_text_to_speech('de_DE')

    def listen(self, duration, sample_rate):
        """ with sr.Microphone() as source:
            print("Bitte sprechen Sie...")
            return self.recognizer.listen(source, phrase_time_limit=5) """
        
        print("Bitte sprechen Sie...")
        recording = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype='float64')
        sd.wait()

        folder_path = os.path.dirname(config.RECORD_TMP_PATH)
        os.makedirs(folder_path, exist_ok=True)

        with wave.open(config.RECORD_TMP_PATH, 'wb') as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(sample_rate)
            wf.writeframes((recording * 32767).astype(np.int16).tobytes())
        return recording.flatten()

    def recognize(self, signal, sample_rate):
        # audio_data = sr.AudioData(signal.tobytes(), sample_rate, 1)
        with sr.AudioFile(config.RECORD_TMP_PATH) as source:
            audio_data = self.recognizer.record(source)
            try:
                text = self.recognizer.recognize_google(audio_data, language=self.language)
                print("Sie haben gesagt: " + text)
                return text
            except sr.UnknownValueError:
                print("Entschuldigung, ich konnte die Audioaufnahme nicht verstehen.")
                return None
            except sr.RequestError as e:
                print("Konnte keine Ergebnisse anfordern; {0}".format(e))
                return None
            
    def text_to_speech(self, satz):
        """ self.pyttsx3.setProperty('rate', 150)
        self.pyttsx3.setProperty('volume', 1)
        self.pyttsx3.say(satz)
        self.pyttsx3.runAndWait() """

        folder_path = os.path.dirname(config.SPEECH_TMP_PATH)
        os.makedirs(folder_path, exist_ok=True)

        tts = gTTS(text=satz, lang='de')
        tts.save(config.SPEECH_TMP_PATH)
        os.system("start " + config.SPEECH_TMP_PATH)
        
    """ def set_sprache_text_to_speech(self, language_code):
        voices = self.pyttsx3.getProperty('voices')
        for voice in voices:
            if language_code in voice.languages:
                self.pyttsx3.setProperty('voice', voice.id)
                break """
