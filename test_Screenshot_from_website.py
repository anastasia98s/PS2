import time
import os
from playwright.sync_api import sync_playwright
from test_read_urls_from_path import read_urls_from_file
from urllib.parse import urlparse

def capture_screenshot(url, save_path):
    try:
        with sync_playwright() as p:
            # Browser (Firefox) starten
            browser = p.firefox.launch(headless=True)  # Du kannst zu "p.chromium" wechseln, wenn du lieber Chromium verwenden möchtest.
            
            # Erstellen eines neuen Browser-Kontexts mit speziellem User-Agent, um HTTP/1.1 zu erzwingen
            context = browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
            )
            page = context.new_page()

            # Webseite aufrufen und warten, bis alle Netzwerkanfragen abgeschlossen sind ("networkidle")
            print(f"Lade URL: {url}")
            page.goto(url, wait_until="networkidle")  # Warten, bis alle Netzwerkanfragen abgeschlossen sind

            # 5 Sekunden zusätzlich warten, um sicherzustellen, dass die Seite vollständig geladen ist
            time.sleep(5)

            # Erstellen eines Dateinamens basierend auf der URL
            parsed_url = urlparse(url)
            hostname = parsed_url.hostname.replace('.', '_')  # Ersetzt Punkte im Hostnamen, damit der Dateiname gültig ist
            screenshot_file = f"{hostname}.png"

            # Vollständigen Pfad zum Screenshot erstellen
            full_save_path = os.path.join(save_path, screenshot_file)
            print(f"Speichere Screenshot: {full_save_path}")

            # Screenshot der gesamten Seite machen und speichern
            page.screenshot(path=full_save_path, full_page=True)

            # Browser schließen
            browser.close()

    except Exception as e:
        print(f"Fehler beim Verarbeiten der URL {url}: {e}")

# Beispielverwendung
if __name__ == '__main__':
    file_path = 'urls_extrahiert.txt'  # Dateipfad zu deiner Datei mit URLs
    urls = read_urls_from_file(file_path)
    print(f"Gefundene URLs: {urls}")
    
    save_path = 'Screenshots_website'  # Ordner, in dem die Screenshots gespeichert werden

    # Verzeichnis erstellen, falls es nicht existiert
    if not os.path.exists(save_path):
        os.makedirs(save_path)
        print(f"Verzeichnis '{save_path}' wurde erstellt.")

    counter= 0
    # Screenshots für jede URL aufnehmen
    for url in urls:
        counter = counter + 1 
        capture_screenshot(url, save_path)
        if(counter==10):
            break