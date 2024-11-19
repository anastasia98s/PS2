from intents.datenkonverter import Datenkonverter

class DatumIntent(Datenkonverter):
    def __init__(self, processor_class_engine):
        super().__init__()
        self.processor_class_engine = processor_class_engine
    
    def abfragen(self, i_datum): # Welches Datum ist morgen/heute/gestern/am Sonntag..
        if self.processor_class_engine.thread_event.is_set():
            return None, None
        
        datum, errortyp = super().date_konverter(i_datum)
        if not datum:
            return None, errortyp
        else:
            datum = datum.strftime("%d. %B %Y")
        
        return f"{i_datum} ist {datum}", None