from test_STT import transcribe_audio
from llama_anfrage import get_chat_response
from test_regEx import search_keywords


def klassifizierung(pfad_audio_datei):
    # Beispiel-Aufruf der Funktion
    file_path = r"C:\Users\KIUser\Documents\Sprachassistent\Intent_wetter.m4a"
    text = transcribe_audio(file_path)

    # LLM-Modelaufruf 
    antwort = get_chat_response("llama3.2", f"Klassifiziere folgenden Text: {text} \
                                in eine der folgenden Klassen: ['Wetter', 'pdf-Auslesen', 'Todos_erzeugen', 'Wikipedia'], \
                                gib mir nur das wort Wetter, pdf-Auslesen, Todos-erzeugen oder Wikipedia aus. ")
    print("Antwort:", antwort)

    klassifizierte_Antwort = search_keywords(antwort)

    with open ('Klassifizierung.txt', 'w') as f:
        f.write(str(klassifizierte_Antwort))
    
    return klassifizierte_Antwort


print(f"Die Audio-Datei gehört zu folgender Klasse: {klassifizierte_Antwort}")