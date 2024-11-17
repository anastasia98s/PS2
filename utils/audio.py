import wave
import numpy as np
import pyttsx3
import os
import config
import librosa
import whisper
import re
import pyaudio
import time
import threading
from nn_aktivierungswort.predictor import Predictor as PredictorAktivierungswort

class Audio:
    def __init__(self):
        self.recognizer = whisper.load_model(config.SPEECH_RECOGNITION_MODELL, config.DEVICE)
        self.pyttsx3 = pyttsx3.init()
        self.set_sprache_text_to_speech(config.MICROSOFT_SPEECH)
        self.wake_word_recognize_stoppen = threading.Event()
        self.predictor_aktivierungswort = PredictorAktivierungswort(config.AKTIVIERUNGSWORT_TRAINED_PATH)

    def listen(self, silence_duration, sample_rate, ohne_init=False):
        self.audio = pyaudio.PyAudio()
        chunk = 1024
        stream = self.audio.open( format=pyaudio.paInt16,
                                    channels=1,
                                    rate=sample_rate,
                                    input=True,
                                    frames_per_buffer=chunk)

        recording = []
        silent_chunks = 0
        silence_limit = int(silence_duration * sample_rate)
        last_chunks = None
        is_recording = True

        recording_runden = 1
        recording_animation_index = 0
        recording_start_time = None
        
        while is_recording:

            if not ohne_init:
                if self.wake_word_recognize_stoppen.is_set():
                    return None, None
            
            try:
                audio_chunk = stream.read(chunk)
                audio_data = np.frombuffer(audio_chunk, dtype=np.int16)
                amplitude = np.abs(audio_data).mean()

                if recording_runden % 5 == 0 or recording_runden == 1:
                    if recording_animation_index == 5:
                        recording_animation_index = 0
                    print("\r", "Frame: " + str(len(recording)) + " |Amplitude: " + str(round(amplitude)) +" |Bitte sprechen Sie" + "." * recording_animation_index, end="", flush=True)
                    recording_animation_index += 1
                recording_runden += 1

                if amplitude > config.AUDIO_THRESHOLD:
                    if not recording_start_time:
                        recording_start_time = time.time()
                    if not recording and last_chunks is not None:
                        recording.append(last_chunks)
                    recording.append(audio_chunk)
                    silent_chunks = 0
                else:
                    if recording_start_time is not None:
                        silent_chunks += len(audio_chunk)
                        if ((time.time() - recording_start_time) > config.MAX_RECORDING_TIME or silent_chunks > silence_limit) and recording:
                            recording.append(audio_chunk)
                            print("\nAufnahme beendet")
                            print("Warte kurz…")
                            is_recording = False
                        elif recording:
                            recording.append(audio_chunk)

                last_chunks = audio_chunk
                # time.sleep(0.01)
            except KeyboardInterrupt:
                is_recording = False

        stream.stop_stream()
        stream.close()
        self.audio.terminate()

        recording_concat = np.concatenate([np.frombuffer(chunk, dtype=np.int16) for chunk in recording])

        # Audioqualität testen
        folder_path = os.path.dirname(config.RECORD_TMP_PATH)
        os.makedirs(folder_path, exist_ok=True)
        with wave.open(config.RECORD_TMP_PATH, 'wb') as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(sample_rate)
            wf.writeframes(recording_concat.tobytes())

        recording_flat = recording_concat.flatten().astype(np.float32)
        recording_trim, _ = librosa.effects.trim(recording_flat, top_db=config.AUDIO_DB)
        return recording_flat, recording_trim

    def recognize(self, signal):
        if self.wake_word_recognize_stoppen.is_set():
            return None
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
                
    def text_to_speech(self, satz):
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

    def listen_recognize(self, silence_duration, sample_rate):
        self.wake_word_recognize_stoppen.clear()
        while True:
            antwort_signal, antwort_signal_trim = self.listen(silence_duration, sample_rate)
            antwort_text = self.recognize(antwort_signal)
            if not antwort_text:
                self.text_to_speech("nochmal bitte")
            else:
                antwort_text = re.sub(r'[.!?]$', '', antwort_text)
                print("Sie haben gesagt: " + antwort_text)
                break

        return antwort_signal_trim, antwort_text
        
    def wake_word_recognize(self, silence_duration, sample_rate):
        self.wake_word_recognize_stoppen.clear()
        lock = threading.Lock()

        def recognize_thread(antwort_signal):
            with lock:
                if antwort_signal is not None and antwort_signal.any() and not self.wake_word_recognize_stoppen.is_set():
                    pred_aktivierung_label = self.predictor_aktivierungswort.predict(antwort_signal)
                    if pred_aktivierung_label == 1:
                        self.wake_word_recognize_stoppen.set()
        threads = []
        while True:
            antwort_signal, antwort_signal_trim = self.listen(config.AKTIVIERUNGSWORT_AUFNAHME_DAUER, sample_rate)

            if not self.wake_word_recognize_stoppen.is_set():
                if antwort_signal_trim is not None:
                    thread = threading.Thread(target=recognize_thread, args=(antwort_signal_trim,))
                    thread.start()
                    threads.append(thread)
            else:
                break
        
        for t in threads:
            t.join()


        self.text_to_speech("Ja?")
        antwort_signal_trim, antwort_text = self.listen_recognize(silence_duration, sample_rate)

        return antwort_signal_trim, antwort_text