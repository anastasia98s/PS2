import sounddevice as sd
import wave
import numpy as np
from gtts import gTTS
import pyttsx3
import os
import config
import librosa
import whisper
import re

class Audio:
    def __init__(self):
        self.recognizer = whisper.load_model(config.SPEECH_RECOGNITION_MODELL, config.DEVICE)
        self.pyttsx3 = pyttsx3.init()
        self.set_sprache_text_to_speech('Microsoft Hedda Desktop - German')

    def listen(self, silence_duration, sample_rate):
        print("Bitte sprechen Sie...")

        recording = []
        silent_chunks = 0
        silence_limit = int(silence_duration * sample_rate)
        last_chunks = None

        is_recording = True
        while is_recording:
            audio_chunk = sd.rec(int(sample_rate * 1), samplerate=sample_rate, channels=1, dtype='float64')
            sd.wait()
            # print(np.abs(audio_chunk).mean())
            if np.abs(audio_chunk).mean() > config.AUDIO_THRESHOLD:
                if not recording and last_chunks is not None:
                    recording.append(last_chunks)
                recording.append(audio_chunk)
                silent_chunks = 0
            else:
                silent_chunks += len(audio_chunk)
                if silent_chunks > silence_limit and recording:
                    print("Aufnahme beenden")
                    is_recording = False
                elif recording:
                    recording.append(audio_chunk)

            last_chunks = audio_chunk

        recording_concat = np.concatenate(recording)
        
        if config.IS_ONLINE:
            folder_path = os.path.dirname(config.RECORD_TMP_PATH)
            os.makedirs(folder_path, exist_ok=True)

            with wave.open(config.RECORD_TMP_PATH, 'wb') as wf:
                wf.setnchannels(1)
                wf.setsampwidth(2) # 16-bit PCM
                wf.setframerate(sample_rate)
                wf.writeframes((recording_concat * 32767).astype(np.int16).tobytes())

        recording_flat = recording_concat.flatten()
        recording_trim, _ = librosa.effects.trim(recording_flat, top_db=config.AUDIO_DB)
        return recording_flat, recording_trim

    def recognize(self, signal):
        signal = signal.astype(np.float32)
        signal = whisper.pad_or_trim(signal)
        result = self.recognizer.transcribe(signal, language="de")
        sr_text = result["text"]
        if sr_text:
            no_speech_prob = result['segments'][0]['no_speech_prob']
            if no_speech_prob < config.NO_SPEECH_MAX_NOTEN:
                return sr_text.strip()
            else:
                return None
        else:
            return None
                
    def text_to_speech(self, satz):
        if config.IS_ONLINE:
            folder_path = os.path.dirname(config.RECORD_TMP_PATH)
            os.makedirs(folder_path, exist_ok=True)

            tts = gTTS(text=satz, lang='de')
            tts.save(config.RECORD_TMP_PATH)
            os.system("start " + config.RECORD_TMP_PATH)
        else:
            self.text_to_speech_await(satz)

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

    def listen_recognize(self, duration, sample_rate):
        while True:
            antwort_signal, antwort_signal_trim = self.listen(duration, sample_rate)
            antwort_text = self.recognize(antwort_signal)
            ohne_zeichen_antwort_text = re.sub(r'[^a-zA-Z0-9\s]', '', antwort_text)
            if not antwort_text:
                self.text_to_speech_await("nochmal bitte")
            else:
                print("Sie haben gesagt: " + antwort_text)
                break

        return antwort_signal_trim, ohne_zeichen_antwort_text