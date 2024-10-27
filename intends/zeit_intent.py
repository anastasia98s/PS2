from datetime import datetime

class ZeitIntent:
    def __init__(self):
        self.time = datetime.now()

    def abfragen(self, i_ort):
        zeit = self.time.strftime("%H:%M")
        if i_ort:
            return f"In {i_ort} ist es jetzt um {zeit}"
        else:
            return f"Jetzt ist es um {zeit}"