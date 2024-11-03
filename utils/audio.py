import speech_recognition as sr
import sounddevice as sd
import wave
import numpy as np
from gtts import gTTS
import pyttsx3
import os
import config
import librosa
import json
from vosk import Model, KaldiRecognizer
from pathlib import Path

class Audio:
    def __init__(self):
        if config.IS_ONLINE:
            self.recognizer = sr.Recognizer()
        else:
            self.download_sr_modell()
            self.model = Model(f"{config.SPEECH_RECOGNITION_MODELL_DIR}{config.SPEECH_RECOGNITION_MODELL}")
            self.recognizer = KaldiRecognizer(self.model, config.AUDIO_SAMPLE_RATE)

        self.pyttsx3 = pyttsx3.init()
        self.set_sprache_text_to_speech('Microsoft Hedda Desktop - German')

    def download_sr_modell(self):
        speech_model_zip = f"{config.SPEECH_RECOGNITION_MODELL}.zip"
        speech_model_url = f"https://alphacephei.com/vosk/models/{speech_model_zip}"
        speech_model_ext_dir_path = Path(f"{config.SPEECH_RECOGNITION_MODELL_DIR}{config.SPEECH_RECOGNITION_MODELL}")
        speech_model_zip_path = Path(f"{config.SPEECH_RECOGNITION_MODELL_DIR}{speech_model_zip}")

        if speech_model_ext_dir_path.is_dir():
            print(f"{speech_model_ext_dir_path.name} exists")
        else:
            import requests
            print(f"Downloading {speech_model_zip_path.name}")
            response = requests.get(speech_model_url)

            if response.status_code == 200:
                with open(speech_model_zip_path, "wb") as f:
                    f.write(response.content)
                print(f"Downloaded {speech_model_zip_path.name}")

                import zipfile
                with zipfile.ZipFile(speech_model_zip_path, 'r') as zip_ref:
                    zip_ref.extractall(config.SPEECH_RECOGNITION_MODELL_DIR)

                os.remove(speech_model_zip_path)
            else:
                print(f"Failed to download {speech_model_zip_path.name}, status code: {response.status_code}")

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
        if config.IS_ONLINE:
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
            try:
                signal = (signal * 32767).astype(np.int16)
                if self.recognizer.AcceptWaveform(signal.tobytes()):
                    text_result = json.loads(self.recognizer.Result())
                    return text_result.get("text", None)
                else:
                    partial_result = json.loads(self.recognizer.PartialResult())
                    self.recognizer.Reset()
                    return partial_result.get("partial", None)
            except json.JSONDecodeError:
                print("Error JSON")
                return None
            except Exception as e:
                print(f"Error: {e}")
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

            if not antwort_text:
                self.text_to_speech_await("nochmal bitte")
            else:
                print("Sie haben gesagt: " + antwort_text)
                break

        return antwort_signal_trim, antwort_text