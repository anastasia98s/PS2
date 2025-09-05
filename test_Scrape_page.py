from playwright.sync_api import sync_playwright
import pytesseract
from PIL import Image
from Test_pytesseract import ocr_test
from DuckduckgoAPI.Tests.test_Screenshot_from_website import capture_screenshot
from Test_llama import get_chat_response
from DuckduckgoAPI.Tests.test_Dateien_in_Verzeichnis import liste_dateien_im_verzeichnis
import os

def scrape_page_with_ocr(Dateiname):
    # OCR-Funktion testen
    text= ocr_test(Dateiname)
    return text

if __name__ == '__main__':
    '''
     # Beispielverwendung
    relatives_verzeichnis = r'.\Screenshots_website'
    dateien = liste_dateien_im_verzeichnis(relatives_verzeichnis)
    print(f"Gefundene Dateien: {dateien}")
    
   
    for img in dateien:
        # Concatenate folder and filename
        file_path = os.path.join(r'Screenshots_website', img)
        extracted_text = scrape_page_with_ocr(file_path)
        print(extracted_text)
        
        os.makedirs('tesseract_extract', exist_ok=True)
        os.makedirs('Antwort', exist_ok=True)
    '''
   # Beispielverwendung
    relatives_verzeichnis = r'.\tesseract_extract'
    dateien = liste_dateien_im_verzeichnis(relatives_verzeichnis)
    print(f"Gefundene Dateien: {dateien}")
    
    
    '''
    with open(fr'tesseract_extract\{img}.txt', 'w', encoding="utf-8") as f:
        f.write(extracted_text)
        # Beispiel-Aufruf der Funktion
        antwort = get_chat_response("llama3.2", f"Wie ist das Wetter \
            heute in Berlin Extrahiere \
            hier die Antwort raus: {extracted_text} \
            formatiere die Antwort im Asciidoc-format.")
        
        with open(fr'Antwort\{img}.txt', 'w') as f:
            f.write(antwort)
    
    ''' 
    
       
    

    
  