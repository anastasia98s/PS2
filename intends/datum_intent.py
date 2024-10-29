#from datetime import datetime, timedelta
from intends.datenkonverter import Datenkonverter

class DatumIntent(Datenkonverter):
    def __init__(self):
        pass
    
    def abfragen(self, i_datum): # Welches Datum ist morgen/heute/..
        """ datezeit = datetime.now()

        if i_datum.lower() == "morgen":
            datezeit = datezeit + timedelta(days=1)

        datum = datetime.strftime(datezeit, "%d %B %Y") """

        datum = super().date_konverter(i_datum).strftime("%Y-%m-%d")

        return f"{i_datum} ist {datum}"