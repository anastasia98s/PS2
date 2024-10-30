import pytesseract
from PIL import Image
from test_Dateien_in_Verzeichnis import liste_dateien_im_verzeichnis
import os 

# Optional: Pfad zu deiner Tesseract-Installation angeben (falls nicht im Systempfad)
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def ocr_test(image_path):
    # Öffne das Bild mit Pillow
    img = Image.open(image_path)

    # Verwende pytesseract, um den Text aus dem Bild zu extrahieren
    text = pytesseract.image_to_string(img)

    return text 
  

if __name__ == "__main__":
    # Beispielverwendung
    relatives_verzeichnis = r'.\Screenshots_website'
    dateien = liste_dateien_im_verzeichnis(relatives_verzeichnis)
    print(f"Gefundene Dateien: {dateien}")
    
    os.makedirs('tesseract_extract', exist_ok=True)

    for img in dateien:
        # Concatenate folder and filename
        file_path = os.path.join(r'Screenshots_website', img)
        extracted_text = ocr_test(file_path)
        with open(fr'tesseract_extract\{img}.txt', 'w') as f:
            f.write(extracted_text)
            
     
        
    
