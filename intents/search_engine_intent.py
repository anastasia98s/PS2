from bs4 import BeautifulSoup
import config
from urllib.parse import quote
from intents.datenkonverter import Datenkonverter
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

class SearchEngineIntent(Datenkonverter):
    def __init__(self, system_presenter):
        self.gesuchte_websites_list = []
        self.gesuchte_websites_index = 0
        self.system_presenter = system_presenter
        self.driver = None

    def get_websites(self, i_thema):
        self.gesuchte_websites_list = []

        thema_urlencode = quote(i_thema)
        content = super().web_indexing(f"https://www.google.com/search?q={thema_urlencode}")

        soup = BeautifulSoup(content, 'html.parser')
        for website in soup.find_all('a', attrs={'jsname': 'UWckNb'}):
            website_title = website.find('h3').text.strip() if website.find('h3') else "Kein Titel"
            website_url = website['href']
            self.gesuchte_websites_list.append((website_title, website_url))

    def website_oeffnen(self):
        website_titel, website_url = self.gesuchte_websites_list[self.gesuchte_websites_index]
        options = Options()
        options.headless = False
        driver = webdriver.Chrome() # service=Service(ChromeDriverManager().install()), options=options
        driver.get(website_url)
        self.driver = driver
        print("Link:", website_url)
        return f"der Titel is {website_titel}", None
    
    ########################################################

    # von system_intent aufgerufen
    def aktion_zurueckgehen(self):
        self.gesuchte_websites_index -= 1
        return self.website_oeffnen()

    # von system_intent aufgerufen
    def aktion_weitergehen(self):
        self.gesuchte_websites_index += 1
        return self.website_oeffnen()
    
    # von system_intent aufgerufen
    def aktion_wiederholen(self):
        self.website_oeffnen()
        return "Website wurde aktualisiert", None
    
    # von system_intent aufgerufen
    def aktion_abbrechen(self):
        if self.driver:
            self.driver.quit()
            return "website wurde geschlosses", None
        else:
            return "kein Vorgang gefunden", None
    
    ########################################################

    # von engine aufgerufen
    def abfragen(self, i_thema):

        if not i_thema:
            return None, config.ERROR_VARIABLE_THEMA # frage nochmal zum Thema
        
        self.system_presenter.intent_presenter = self # bei system_intent anmelden
        self.get_websites(i_thema)
        return self.website_oeffnen()