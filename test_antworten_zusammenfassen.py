from test_llama import get_chat_response

from test_Dateien_in_Verzeichnis import liste_dateien_im_verzeichnis


relatives_verzeichnis = 'responses'
dateien = liste_dateien_im_verzeichnis(relatives_verzeichnis)
print(f"Gefundene Dateien: {dateien}")


for datei in dateien:
    with open(fr'responses\{datei}', 'r') as f:
        text= f.read()
        
        response= get_chat_response("llama3.2",  f'Wie ist das Wetter heute in berlin? Beantworte die Frage, beziehe den {text}\
            für deine Antwort mit ein. Lasse das wort true weg, antworte in maximal 3 sätzen!')
        print(response)