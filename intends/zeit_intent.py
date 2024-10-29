from datetime import datetime

class ZeitIntent:
    def __init__(self):
        self.time = datetime.now()
        
    # Override
    def abfragen(self, i_ort): # Wie spät in Berlin
        zeit = self.time.strftime("%H:%M")
        if i_ort:
            return f"In {i_ort} ist es jetzt um {zeit}"
        else:
            return f"Jetzt ist es um {zeit}"