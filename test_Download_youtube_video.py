from pytube import YouTube

# Liste der YouTube-URLs
video_urls = [
    "https://www.youtube.com/watch?v=7Lu7lHBY4Ws",
    "https://www.youtube.com/watch?v=3mOx2wPUdqI"
]

# Funktion zum Herunterladen der Audiodatei
def download_audio(video_url):
    try:
        yt = YouTube(video_url)
        # Filtern und den ersten Audio-Stream auswählen
        downloader = yt.streams.filter(only_audio=True).first()

        # Herunterladen der Audiodatei
        downloader.download()

        print(f"Audio erfolgreich von {video_url} heruntergeladen.")
    except Exception as e:
        print(f"Fehler beim Herunterladen von {video_url}: {e}")

# Iterieren über die Liste von YouTube-URLs und Audiodateien herunterladen
for url in video_urls:
    download_audio(url)

print("Alle Audiodateien wurden heruntergeladen!")