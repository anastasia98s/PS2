from bs4 import BeautifulSoup
import os
import yt_dlp
import subprocess
import config
from urllib.parse import quote
from intents.datenkonverter import Datenkonverter
from intents.datenkonverter import Datenkonverter
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

class YoutubeIntent(Datenkonverter):
    def __init__(self, system_presenter, text_to_speech):
        self.driver = None
        self.gesuchte_videos_list = []
        self.gesuchte_videos_index = 0
        self.YOUTUBE_FILE_PATH = f"{config.YOUTUBE_FILE_DIR}/{config.YOUTUBE_FILE_NAME}"
        self.system_presenter = system_presenter
        self.text_to_speech = text_to_speech

    def get_videos(self, i_thema):
        self.text_to_speech.text_to_speech(f"Suche nach {i_thema} auf YouTube")
        self.gesuchte_videos_list = []

        thema_urlencode = quote(i_thema)
        content = super().web_indexing(f"https://www.youtube.com/results?search_query={thema_urlencode}")

        soup = BeautifulSoup(content, 'html.parser')
        for video in soup.find_all('a', id='video-title'):
            video_title = video['title']
            video_url = video['href']
            if 'v=' in video_url:
                video_id = video_url.split('v=')[1].split('&')[0]
                self.gesuchte_videos_list.append((video_title, video_id))

    def download_video_as_audio(self):
        if len(self.gesuchte_videos_list) > 0:
            video_titel, video_id = self.gesuchte_videos_list[self.gesuchte_videos_index]
            
            video_url = f"https://www.youtube.com/watch?v={video_id}"
            try:

                with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
                    video_info = ydl.extract_info(video_url, download=False)
                    video_duration = video_info.get('duration', 0)
                    is_live = video_info.get('is_live', False)

                    if is_live:
                        print(f"{video_titel} ist ein Livestream. Download abgebrochen.")
                        return f"Dieses Video ist zu lang", 2
                        
                    self.text_to_speech.text_to_speech(f"{video_titel} herunterladen")
                    if video_duration > config.MAX_YOUTUBE_FILE * 60:
                        print(f"{video_titel} ist zu lang (>{config.MAX_YOUTUBE_FILE} Minuten). Download abgebrochen.")
                        return f"Dieses Video ist zu lang", 2
                if os.path.exists(self.YOUTUBE_FILE_PATH):
                    os.remove(self.YOUTUBE_FILE_PATH)

                ydl_opts = {
                    'format': 'bestaudio/best',
                    'extractaudio': True,
                    'outtmpl': os.path.join(config.YOUTUBE_FILE_DIR, '%(title)s.%(ext)s'),
                }
                
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([video_url])

                downloaded_file = [f for f in os.listdir(config.YOUTUBE_FILE_DIR) if f.endswith(('.webm', '.m4a'))]
                
                if downloaded_file:
                    downloaded_file = downloaded_file[0]
                    file_path = os.path.join(config.YOUTUBE_FILE_DIR, downloaded_file)
                    mp3_path = self.YOUTUBE_FILE_PATH

                    subprocess.run(['ffmpeg', '-i', file_path, mp3_path])
                    os.remove(file_path)

                    return f"Audio erfolgreich von {video_titel} heruntergeladen und als MP3 konvertiert.", None
                else:
                    return f"Keine unterstützte Audiodatei von {video_url} gefunden.", 1
            except Exception as e:
                return f"Fehler beim Herunterladen von {video_titel}", 1
        else:
            return f"Ich habe kein Video gefunden.", 1
        
    def video_abspielen(self):
        if len(self.gesuchte_videos_list) > 0:
            # self.text_to_speech.text_to_speech(f"Moment bitte")
            video_titel, video_id = self.gesuchte_videos_list[self.gesuchte_videos_index]
            options = Options()
            options.headless = False
            options.add_argument("--autoplay-policy=no-user-gesture-required")
            driver = webdriver.Chrome(options=options)
            driver.get(f"https://www.youtube.com/embed/{video_id}?autoplay=1")
            self.driver = driver
            return None, None # f"der Titel is {video_titel}"
        else:
            return f"Ich habe kein Video gefunden.", 1

    def video_herunterladen_abspielen(self, is_neues_playlist):
        self.text_to_speech.text_to_speech("suche ein Video zum Herunterladen")
        message = None
        while True:
            message, error = self.download_video_as_audio()
            if error == 2 and is_neues_playlist:
                self.text_to_speech.text_to_speech(f"Such nach einem anderen Video, denn {message}")
                del self.gesuchte_videos_list[self.gesuchte_videos_index]
            else:
                break
        if not error:
            # self.prozess = subprocess.Popen("start " + self.YOUTUBE_FILE_PATH, shell=True)
            os.system("start " + self.YOUTUBE_FILE_PATH)
            return None, None
        else:
            return message, None
    
    ########################################################

    # von system_intent aufgerufen
    def aktion_zurueckgehen(self):
        self.gesuchte_videos_index -= 1
        return self.video_abspielen()

    # von youtube_intent & system_intent aufgerufen
    def aktion_weitergehen(self):
        self.gesuchte_videos_index += 1
        return self.video_abspielen()
    
    # von system_intent aufgerufen
    def aktion_wiederholen(self):
        return self.video_abspielen()
    
    # von system_intent aufgerufen
    def aktion_abbrechen(self):
        if self.driver:
            self.driver.quit()
            self.driver = None
            return "das Video wurde geschlossen", None
        else:
            return "kein Vorgang gefunden", None
            
    ########################################################

    # von engine aufgerufen
    def abfragen(self, i_thema):

        if not i_thema:
            return None, config.ERROR_VARIABLE_THEMA # frage nochmal zum Thema
        
        self.system_presenter.intent_presenter = self # bei system_intent anmelden
        self.get_videos(i_thema)
        return self.video_abspielen()
    
    # von engine aufgerufen
    def herunterladen(self, i_thema):
        is_neues_playlist = None
        if i_thema:
            self.system_presenter.intent_presenter = self
            self.get_videos(i_thema)
            is_neues_playlist = 1
            
        return self.video_herunterladen_abspielen(is_neues_playlist)