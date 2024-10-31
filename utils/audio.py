import speech_recognition as sr
import sounddevice as sd
import wave
import numpy as np
from gtts import gTTS
import pyttsx3
import os
import config
import librosa

class Audio:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.pyttsx3 = pyttsx3.init()
        self.set_sprache_text_to_speech('Microsoft Hedda Desktop - German')

    def listen(self, silence_duration, sample_rate, record_path):
        """ with sr.Microphone() as source:
            print("Bitte sprechen Sie...")
            return self.recognizer.listen(source, phrase_time_limit=5) """
        
        """ print("Bitte sprechen Sie...")
        recording = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype='float64')
        sd.wait() """

        print("Bitte sprechen Sie...")

        recording = []
        silent_chunks = 0
        silence_limit = int(silence_duration * sample_rate)

        is_recording = True
        while is_recording:
            audio_chunk = sd.rec(int(sample_rate * 1), samplerate=sample_rate, channels=1, dtype='float64')
            sd.wait()
            print(np.abs(audio_chunk).mean())
            if np.abs(audio_chunk).mean() > config.AUDIO_THRESHOLD:
                recording.append(audio_chunk)
                silent_chunks = 0
            else:
                silent_chunks += len(audio_chunk)
                if silent_chunks > silence_limit and recording:
                    print("Aufnahme beenden")
                    is_recording = False

        recording_concat = np.concatenate(recording)

        folder_path = os.path.dirname(record_path)
        os.makedirs(folder_path, exist_ok=True)

        with wave.open(record_path, 'wb') as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2) # 16-bit PCM
            wf.setframerate(sample_rate)
            wf.writeframes((recording_concat * 32767).astype(np.int16).tobytes())

        recording_flat = recording_concat.flatten()
        recording_trim, _ = librosa.effects.trim(recording_flat, top_db=config.AUDIO_DB)
        return recording_trim

    def recognize(self, signal, sample_rate, record_path):
        # audio_data = sr.AudioData(signal.tobytes(), sample_rate, 1)
        with sr.AudioFile(record_path) as source:
            audio_data = self.recognizer.record(source)
            try:
                text = self.recognizer.recognize_google(audio_data, language=config.AUDIO_SPRACHE)
                print("Sie haben gesagt: " + text)
                return text
            except sr.UnknownValueError:
                print("Entschuldigung, ich konnte die Audioaufnahme nicht verstehen.")
                return None
            except sr.RequestError as e:
                print("Konnte keine Ergebnisse anfordern; {0}".format(e))
                return None
            
    def text_to_speech(self, satz, record_path):
        folder_path = os.path.dirname(record_path)
        os.makedirs(folder_path, exist_ok=True)

        tts = gTTS(text=satz, lang='de')
        tts.save(record_path)
        os.system("start " + record_path)

    def text_to_speech_await(self, satz):
        self.pyttsx3.setProperty('rate', 150)
        self.pyttsx3.setProperty('volume', 1)
        self.pyttsx3.say(satz)
        self.pyttsx3.runAndWait()
        
    def set_sprache_text_to_speech(self, speaker_name):
        voices = self.pyttsx3.getProperty('voices')
        for voice in voices:
            # print(voice)
            if speaker_name in voice.name:
                self.pyttsx3.setProperty('voice', voice.id)
                break

    def listen_recognize(self, duration, sample_rate, record_path):
        antwort_text = None
        while antwort_text is None:
            antwort_signal = self.listen(duration, sample_rate, record_path)
            antwort_text = self.recognize(antwort_signal, sample_rate, record_path)
            if not antwort_text:
                self.text_to_speech_await("nochmal bitte")
        return antwort_signal, antwort_text