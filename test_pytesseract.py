import pytesseract
from PIL import Image

# Optional: Pfad zu deiner Tesseract-Installation angeben (falls nicht im Systempfad)
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def ocr_test(image_path):
    # Öffne das Bild mit Pillow
    img = Image.open(image_path)

    # Verwende pytesseract, um den Text aus dem Bild zu extrahieren
    text = pytesseract.image_to_string(img)

    return text 
  

if __name__ == "__main__":
    # Bildpfad angeben (z. B. 'test_image.png')
    image_path = 'image.png'
   

    # OCR-Funktion testen
    text= ocr_test(image_path)
       # Extrahierten Text ausgeben
    print("Erkannter Text:")
    print(text)
    
    ### Manuell getestet und bestanden!!! ;) 