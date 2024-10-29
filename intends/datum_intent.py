from datetime import datetime, timedelta

class DatumIntent:
    def __init__(self):
        pass
    
    # Override
    def abfragen(self, i_datum): # Welches Datum ist morgen/heute/..
        datezeit = datetime.now()

        if i_datum.lower() == "morgen":
            datezeit = datezeit + timedelta(days=1)

        datum = datetime.strftime(datezeit, "%d %B %Y")
        return f"{i_datum} ist {datum}"