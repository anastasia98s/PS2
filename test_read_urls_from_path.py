def read_urls_from_file(file_path):
    urls = []
    with open(file_path, 'r') as file:
        # Jede Zeile der Datei durchlaufen
        for line in file:
            url = line.strip()  # Leerzeichen und Zeilenumbrüche entfernen
            if url:  # Nur nicht-leere Zeilen hinzufügen
                urls.append(url)
    return urls

# Beispielverwendung
if __name__ == '__main__':
    file_path = 'urls_extrahiert.txt'  # Dateipfad zu deiner Datei mit URLs
    urls = read_urls_from_file(file_path)
    print(urls)