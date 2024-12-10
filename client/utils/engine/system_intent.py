from selenium import webdriver
from selenium.webdriver.chrome.options import Options

class SystemIntent:
    def __init__(self):
        self.driver = None
        self.playlist = []
        self.playlist_index = 0

    def website_oeffnen(self):
        if len(self.playlist) > 0:
            website_titel, website_url = self.playlist[self.playlist_index]
            options = Options()
            options.headless = False
            options.add_argument("--autoplay-policy=no-user-gesture-required")
            driver = webdriver.Chrome(options=options)
            driver.get(website_url)
            self.driver = driver
            print("Link:", website_url)
            return f"der Titel is {website_titel}", None
        else:
            return f"Ich habe kein Playlist gefunden.", None

    def zurueckgehen(self):
        self.playlist_index -= 1
        return self.website_oeffnen()
        
    def weitergehen(self):
        self.playlist_index += 1
        return self.website_oeffnen()
    
    def wiederholen(self):
        if hasattr(self, 'driver') and self.driver:
            try:
                self.driver.refresh()
                return "Die Webseite wurde erfolgreich aktualisiert", None
            except Exception:
                return "Der Browser wurde geschlossen. Bitte starten Sie ihn erneut.", None
        else:
             return "Kein aktiver Webdriver gefunden. Bitte zuerst eine Webseite öffnen", None
    
    def abbrechen(self):
        if self.driver:
            self.driver.quit()
            self.driver = None
            return "Die Website wurde geschlossen", None
        else:
            return None, None