from test_llama import get_chat_response
from test_Dateien_in_Verzeichnis import liste_dateien_im_verzeichnis
import os 
from test_zustimmen_404 import parse_404_akzeptieren_Zustimmen


relatives_verzeichnis = 'tesseract_extract'
dateien = liste_dateien_im_verzeichnis(relatives_verzeichnis)
print(f"Gefundene Dateien: {dateien}")

responses = []
for datei in dateien:
    with open(fr'tesseract_extract\{datei}', 'r') as f:
        text= f.read()
        matches= parse_404_akzeptieren_Zustimmen(text)
        if (len(matches)>0):
            continue
        
        
        
        response= get_chat_response("llama3.2",  f'Beantworte mir folgende Frage zu dem Text {text} \
                        Wie ist das Wetter in Berlin? Beginne die Anwort mit\
                        dem Wort True,\
                        wenn du denkst, dass diese richtig ist. Anworte mit 2 Sätzen.')
        responses.append(response)
        
        print(responses)

os.makedirs('responses', exist_ok=True)

    
with open(fr"responses\output.txt", "w") as f:
    for item in responses:
        f.write(f"{item}\n")


       
  
        
   