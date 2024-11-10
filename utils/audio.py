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

class Audio:
    def __init__(self):
        self.recognizer = whisper.load_model(config.SPEECH_RECOGNITION_MODELL, config.DEVICE)
        self.pyttsx3 = pyttsx3.init()
        self.set_sprache_text_to_speech(config.MICROSOFT_SPEECH)

    def listen(self, silence_duration, sample_rate):
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
        recording_start_time = time.time()

        while is_recording:
            if recording_runden % 5 == 0 or recording_runden == 1:
                if recording_animation_index == 5:
                    recording_animation_index = 0
                print("\r", end="", flush=True)
                print("Bitte sprechen Sie" + "." * recording_animation_index, end="", flush=True)
                recording_animation_index += 1
            recording_runden += 1
            
            try:
                audio_chunk = stream.read(chunk)
                audio_data = np.frombuffer(audio_chunk, dtype=np.int16)
                amplitude = np.abs(audio_data).mean()
                # print(amplitude)
                if amplitude > config.AUDIO_THRESHOLD:
                    if not recording and last_chunks is not None:
                        recording.append(last_chunks)
                    recording.append(audio_chunk)
                    silent_chunks = 0
                else:
                    silent_chunks += len(audio_chunk)
                    if ((time.time() - recording_start_time) > config.MAX_RECORDING_TIME or silent_chunks > silence_limit) and recording:
                        print("\nAufnahme beendet")
                        print("Warte kurz…")
                        is_recording = False
                    elif recording:
                        recording.append(audio_chunk)

                last_chunks = audio_chunk
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
            wf.setsampwidth(2) # 16-bit PCM
            wf.setframerate(sample_rate)
            wf.writeframes(recording_concat.tobytes())

        recording_flat = recording_concat.flatten().astype(np.float32)
        recording_trim, _ = librosa.effects.trim(recording_flat, top_db=config.AUDIO_DB)
        return recording_flat, recording_trim

    def recognize(self, signal):
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
        while True:
            antwort_signal, antwort_signal_trim = self.listen(silence_duration, sample_rate)
            antwort_text = self.recognize(antwort_signal)
            if not antwort_text:
                self.text_to_speech("nochmal bitte")
            else:
                antwort_text = re.sub(r'[.!?]$', '', antwort_text)
                antwort_text = re.sub(r'(\bum\s*)(\d{1,2})\.(\d{1,2})(?!\s*Uhr)', r'\1\2:\3', antwort_text)
                print("Sie haben gesagt: " + antwort_text)
                break

        return antwort_signal_trim, antwort_text
    
    def wake_word_recognize(self, silence_duration, sample_rate):
        while True:
            antwort_signal, antwort_signal_trim = self.listen(silence_duration, sample_rate)
            antwort_text = self.recognize(antwort_signal)
            if antwort_text:
                print("Sie haben gesagt: " + antwort_text)
                wake_word_pattern = r'\b(?:' + '|'.join(config.WAKE_WORD_ARRAY) + r')\b[.,\s]*'
                if re.search(wake_word_pattern, antwort_text, flags=re.IGNORECASE):
                    wake_word_gruesse_pattern = r'\b(?:' + '|'.join(config.WAKE_WORD_ARRAY + config.WAKE_WORD_GRUESSE_ARRAY) + r')\b[.,\s]*'
                    antwort_text = re.sub(wake_word_gruesse_pattern, '', antwort_text, flags=re.IGNORECASE).strip()
                    antwort_text = re.sub(r'[.!?,]$', '', antwort_text)
                    antwort_text = re.sub(r'(\bum\s*)(\d{1,2})\.(\d{1,2})(?!\s*Uhr)', r'\1\2:\3', antwort_text)
                    if antwort_text:
                        break
                    else:
                        self.text_to_speech("Ja?")
                        self.listen_recognize(silence_duration, sample_rate)
                        break

        return antwort_signal_trim, antwort_text