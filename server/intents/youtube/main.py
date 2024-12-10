import api
from fastapi import FastAPI, Body
import uvicorn
from bs4 import BeautifulSoup
from urllib.parse import quote

app = FastAPI()

@app.post("/youtube_intent/abfragen")
def abfragen(i_thema: str = Body(...)):
    if not i_thema:
        return None, api.ERROR_VARIABLE_THEMA, None
    
    thema_urlencode = quote(i_thema)
    content, error_indexing, error_request = api.web_indexing(f"https://www.youtube.com/results?search_query={thema_urlencode}")
    if error_request:
        return content, None, 1
    
    if error_indexing:
        return "Fehler beim Indizieren", None, 1
    else:
        gesuchte_videos_list = []
        soup = BeautifulSoup(content, 'html.parser')
        for video in soup.find_all('a', id='video-title'):
            video_title = video['title']
            video_url = video['href']
            if 'v=' in video_url:
                video_id = video_url.split('v=')[1].split('&')[0]
                gesuchte_videos_list.append((video_title, f"https://www.youtube.com/embed/{video_id}?autoplay=1"))

        return gesuchte_videos_list, None, None
    
if __name__ == "__main__":
    uvicorn.run("main:app", host=api.YOUTUBE_INTENT_SERVICE_IP, port=api.YOUTUBE_INTENT_SERVICE_PORT)