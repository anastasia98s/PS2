from intends.datenkonverter import Datenkonverter

class DatumIntent(Datenkonverter):
    def __init__(self):
        super().__init__()
    
    def abfragen(self, i_datum): # Welches Datum ist morgen/heute/gestern/am Sonntag..
        datum, errortyp = super().date_konverter(i_datum)
        if not datum:
            return None, errortyp
        else:
            datum = datum.strftime("%d. %B %Y")
            
        return f"{i_datum} ist {datum}", None