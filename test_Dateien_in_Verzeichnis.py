import os

def liste_dateien_im_verzeichnis(relativer_pfad):
    # Absoluten Pfad erzeugen
    absoluter_pfad = os.path.abspath(relativer_pfad)

    # Überprüfen, ob das Verzeichnis existiert
    if not os.path.exists(absoluter_pfad):
        print(f"Das Verzeichnis {absoluter_pfad} existiert nicht. Es wird erstellt.")
        os.makedirs(absoluter_pfad)
    else:
        print(f"Das Verzeichnis {absoluter_pfad} existiert.")

    # Alle Dateien und Unterverzeichnisse im Verzeichnis auflisten
    dateien_und_verzeichnisse = os.listdir(absoluter_pfad)

    # Optional: Nur Dateien auflisten (keine Verzeichnisse)
    nur_dateien = [f for f in dateien_und_verzeichnisse if os.path.isfile(os.path.join(absoluter_pfad, f))]

    return nur_dateien

if __name__ == '__main__':
    # Beispielverwendung
    relatives_verzeichnis = 'DuckduckgoAPI\Screenshots_website'
    dateien = liste_dateien_im_verzeichnis(relatives_verzeichnis)
    print(f"Gefundene Dateien: {dateien}")