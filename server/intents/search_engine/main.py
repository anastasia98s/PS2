import api
from fastapi import FastAPI, Body
import uvicorn
from bs4 import BeautifulSoup
from urllib.parse import quote

app = FastAPI()

@app.post("/search_engine_intent/abfragen")
def abfragen(i_thema: str = Body(...)):
    if not i_thema:
        return None, api.ERROR_VARIABLE_THEMA, None
    
    thema_urlencode = quote(i_thema)
    content, error_indexing, error_request = api.web_indexing(f"https://www.google.com/search?q={thema_urlencode}")
    if error_request:
        return content, None, 1
    
    if error_indexing:
        return "Fehler beim Indizieren", None, 1
    else:
        gesuchte_websites_list = []
        soup = BeautifulSoup(content, 'html.parser')
        for website in soup.find_all('a', attrs={'jsname': 'UWckNb'}):
            website_title = website.find('h3').text.strip() if website.find('h3') else "Kein Titel"
            website_url = website['href']
            gesuchte_websites_list.append((website_title, website_url))

        return gesuchte_websites_list, None, None
    

if __name__ == "__main__":
    uvicorn.run("main:app", host=api.SEARCH_ENGINE_INTENT_SERVICE_IP, port=api.SEARCH_ENGINE_INTENT_SERVICE_PORT)