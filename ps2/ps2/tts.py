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