from datetime import datetime
import pytz

class UhrzeitIntent:
    def __init__(self):
        self.time_zone = {
            "berlin": "Europe/Berlin",
            "new york": "America/New_York",
            "tokyo": "Asia/Tokyo",
            "london": "Europe/London",
            "sydney": "Australia/Sydney",
            "paris": "Europe/Paris",
            "moscow": "Europe/Moscow",
            "dubai": "Asia/Dubai",
            "los angeles": "America/Los_Angeles",
            "rio de janeiro": "America/Sao_Paulo",
            "singapore": "Asia/Singapore",
            "mumbai": "Asia/Kolkata",
            "seoul": "Asia/Seoul",
            "cairo": "Africa/Cairo",
            "mexico city": "America/Mexico_City",
            "cape town": "Africa/Johannesburg"
        }
        
    def abfragen(self, i_ort):
        
        time = datetime.now(pytz.utc)
        if i_ort:
            if i_ort.lower() in self.time_zone:
                timezone = pytz.timezone(self.time_zone[i_ort.lower()])
                time = time.astimezone(timezone)
            else:
                return f"Zeitzone für '{i_ort}' wurde nicht gefunden", None

            zeit = time.strftime("%H:%M")
            return f"In {i_ort} ist es jetzt um {zeit} Uhr", None
        else:
            zeit = time.strftime("%H:%M")
            return f"Jetzt ist es um {zeit} Uhr", None