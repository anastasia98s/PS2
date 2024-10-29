import re

def search_keywords(text):
    # Der reguläre Ausdruck sucht nach den Wörtern "Wetter", "Lego" oder "Aufgaben"
    pattern = r"\b(Wetter|Lego|Aufgaben)\b"
    
    # Suche nach den Wörtern im Text
    matches = re.findall(pattern, text)
    
    return matches

# Beispielaufruf der Funktion
text = "Ich würde den Text 'How is the weather today?' klassifizieren als ['Wetter']."
result = search_keywords(text)

print(result)