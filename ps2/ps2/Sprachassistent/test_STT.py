import whisper

def transcribe_audio(file_path, model_size="large", language="de", task="translate"):
    """
    Transkribiert eine Audiodatei mit Whisper und übersetzt sie ins angegebene Ziel.

    :param file_path: Der Pfad zur Audiodatei (z. B. .m4a, .mp3, .wav).
    :param model_size: Die Größe des Whisper-Modells (z. B. "small", "medium", "large").
    :param language: Die Sprache der Audiodatei (z. B. "de" für Deutsch).
    :param task: Die Aufgabe für das Modell ("transcribe" oder "translate").
    :return: Der transkribierte und/oder übersetzte Text.
    """

    # Modell laden
    model = whisper.load_model(model_size)

    # Optionen festlegen
    options = {"language": language, "task": task}

    # Transkription durchführen
    result = model.transcribe(file_path, **options)

    # Rückgabe des transkribierten Textes
    return result["text"]

# Beispiel-Aufruf der Funktion
file_path = r"C:\Users\KIUser\Documents\Sprachassistent\Intent_wetter.m4a"
text = transcribe_audio(file_path)
print("Transkribierter Text:", text)