from datetime import datetime

class DatumIntent:
    def __init__(self):
        self.datum = datetime.now()

    def abfragen(self, i_datum):
        datum = self.datum.strftime("%d %B %Y")
        return f"{i_datum} ist {datum}"