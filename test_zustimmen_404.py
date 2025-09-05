import re


def parse_404_akzeptieren_Zustimmen(text):
    # Regulärer Ausdruck zum Extrahieren von '404' und 'Zustimmen'
    regex = r'\b(?:404|Zustimmen|Akzeptieren)\b'

    # Suche nach Mustern im Text
    matches = re.findall(regex, text)
    
    return matches


if __name__=="__main__":
    # Beispieltext
    text = "Dieser Text enthält Akzeptieren und Zustimmen und 404."
    matches= parse_404_akzeptieren_Zustimmen(text)
    # Ausgabe der gefundenen Muster
    print(matches)
