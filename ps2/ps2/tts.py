import wave
import librosa
import numpy as np

import pyttsx3
import speech_recognition as sr

def speak(text):
    engine = pyttsx3.init()
    # Set the voice to German
    voices = engine.getProperty('voices')
    for voice in voices:
        if 'de' in voice.languages:  # Check for German language
            engine.setProperty('voice', voice.id)
            break
    engine.say(text)
    engine.runAndWait()

def listen():
    """Listen to the user's speech and convert it to text in German."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Hören...")
        recognizer.adjust_for_ambient_noise(source)  # Adjust for ambient noise
        audio = recognizer.listen(source)

    try:
        # Recognize speech using Google Web Speech API in German
        text = recognizer.recognize_google(audio, language='de-DE')
        print(f"Sie haben gesagt: {text}")
        return text
    except sr.UnknownValueError:
        print("Entschuldigung, ich konnte die Audioaufnahme nicht verstehen.")
        return None
    except sr.RequestError as e:
        print(f"Die Ergebnisse konnten nicht von Google Speech Recognition-Dienst angefordert werden; {e}")
        return None

def record_audio(filename):
        """Record audio from the microphone and save it to a file."""
        recognizer = sr.Recognizer()

        with sr.Microphone() as source:
            print("Bitte sagen Sie Ihren Namen...")

            audio_data = recognizer.listen(source, timeout=5)

            # Save the audio data to a WAV file
            with wave.open(filename, 'wb') as wf:
                wf.setnchannels(1)  # Mono
                wf.setsampwidth(2)  # 16-bit
                wf.setframerate(48000)  # Sample rate
                wf.writeframes(audio_data.get_wav_data())

        print(f"Audio gespeichert in {filename}")


def extract_features(filename):
    """Extract audio features from the recorded audio file."""
    try:
        # Load audio file
        audio_data, sample_rate = librosa.load(filename, sr=None)

        # Check if audio data is empty
        if audio_data.size == 0:
            print("Audio data is empty.")
            return None

        # Extract MFCC features
        mfccs = librosa.feature.mfcc(y=audio_data, sr=sample_rate, n_mfcc=13)

        # Average over time
        mfccs_mean = np.mean(mfccs.T, axis=0)

        return mfccs_mean

    except Exception as e:
        print(f"Error extracting features: {e}")
        return None