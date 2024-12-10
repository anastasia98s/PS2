import pdfplumber
import re

# Convert PDF to a text and remove hyphenation to enhance readability
def convert_to_text(pdf):
    with pdfplumber.open(pdf) as pdf:
        all_text=""
        for page in pdf.pages:
            all_text+=page.extract_text() +"\n"
            all_text=remove_hyphenation(all_text)
        return all_text
    
def remove_hyphenation(text):
    # Entfernt Bindestriche am Zeilenende und verbindet die getrennten Wörter
    # Beispiel: "Beispiel-\ntext" wird zu "Beispieltext"
    cleaned_text = re.sub(r'(\w+)-\n(\w+)', r'\1\2', text)
    
    # Optional: Entfernt auch alle weiteren Zeilenumbrüche, die keine Bindestriche haben
    cleaned_text = re.sub(r'\n', ' ', cleaned_text)  # Entfernt normale Zeilenumbrüche
    
    return cleaned_text