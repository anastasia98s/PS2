import re
from test_read_urls_from_path import read_urls_from_file

def extract_urls(text):
    # Definiere den regulären Ausdruck für URLs
    url_pattern = r'https?://[^\s]+'
    
    # Finde alle Vorkommen des Musters im Text
    urls = re.findall(url_pattern, text)
    
    return urls


if __name__ == '__main__': 
    file_path = 'urls.txt'  # Dateipfad zu deiner Datei mit URLs
    urls = read_urls_from_file(file_path)
    print(urls)
    
    # Liste in einen String konvertieren, wobei jedes Element in einer neuen Zeile steht
    urls_string = "\n".join(urls)
    
    
    # URLs extrahieren
    urls = extract_urls(urls_string)

    # Extrahierte URLs anzeigen
    for url in urls:
        print(url)
        with open('urls_extrahiert.txt', 'a') as f:
            f.write(url + '\n')
     