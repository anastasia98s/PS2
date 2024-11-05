#from datetime import datetime, timedelta
from intends.datenkonverter import Datenkonverter

class DatumIntent(Datenkonverter):
    def __init__(self):
        pass
    
    def abfragen(self, i_datum): # Welches Datum ist morgen/heute/gestern/am Sonntag..
        datum, errortyp = super().date_konverter(i_datum)
        if not datum:
            return None, errortyp
        else:
            datum = datum.strftime("%Y-%m-%d")
            
        return f"{i_datum} ist {datum}", None