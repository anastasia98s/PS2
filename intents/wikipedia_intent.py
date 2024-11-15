import wikipedia

class WikipediaIntent:
    def __init__(self):
        pass
    
    def abfragen(self, i_thema):
        # TODO
        """
            Wenn du zusätzliche Variablen benötigst, 
            kannst du selbstverständlich auch andere Variablen verwenden und nicht nur `i_thema`.
            Die Wahl der Variablen hängt von den Anforderungen und dem Kontext deines Projekts ab.
        """

        #nur Demo
        try:
            wikipedia.set_lang("de")
            return wikipedia.summary(i_thema, sentences=5), None
        except Exception as e:
            return f"Ich weiss {i_thema} nicht", None