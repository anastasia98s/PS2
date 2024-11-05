import wikipedia

class WikipediaIntent:
    def __init__(self):
        pass
    
    def abfragen(self, i_thema):
        try:
            wikipedia.set_lang("de")
            return wikipedia.summary(i_thema, sentences=5), None
        except Exception as e:
            return f"Ich weiss {i_thema} nicht", None