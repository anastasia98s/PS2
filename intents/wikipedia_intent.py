import wikipedia

class WikipediaIntent:
    def __init__(self, processor_class_engine):
        self.processor_class_engine = processor_class_engine
    
    def abfragen(self, i_thema):
        if self.processor_class_engine.thread_event.is_set(): # für Multithreading: du kannst es als default lassen, da es nicht hier kontrolliert wird.
            return None, None
        
        # TODO
        """
            Wenn du zusätzliche Variablen benötigst, 
            kannst du selbstverständlich auch andere Variablen verwenden und nicht nur `i_thema`.
            Die Wahl der Variablen hängt von den Anforderungen und dem Kontext deines Projekts ab.
        """

        try:
            wikipedia.set_lang("de")
            return wikipedia.summary(i_thema, sentences=5), None
        except Exception as e:
            return f"Ich weiss {i_thema} nicht", None