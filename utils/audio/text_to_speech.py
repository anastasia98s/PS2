import pyttsx3
import config
from gtts import gTTS
import os

class TTS:
    def __init__(self):
        #self.pyttsx3 = pyttsx3.init()
        #self.set_sprache_text_to_speech(config.MICROSOFT_SPEECH)
        pass
            
    def text_to_speech(self, satz):
        """ self.pyttsx3.setProperty('rate', 150)
        self.pyttsx3.setProperty('volume', 1)
        self.pyttsx3.say(satz)
        self.pyttsx3.runAndWait() """

        folder_path = os.path.dirname(config.RECORD_TMP_PATH)
        os.makedirs(folder_path, exist_ok=True)
        tts = gTTS(text=satz, lang='de')
        tts.save(config.RECORD_TMP_PATH)
        os.system("start " + config.RECORD_TMP_PATH)
        
    def set_sprache_text_to_speech(self, speaker_name):
        voices = self.pyttsx3.getProperty('voices')
        for voice in voices:
            if speaker_name in voice.name:
                self.pyttsx3.setProperty('voice', voice.id)
                break