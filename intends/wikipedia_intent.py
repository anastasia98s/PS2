import wikipedia

class WikipediaIntent:
    def __init__(self):
        pass
    
    # Override
    def abfragen(self, i_thema): # Wer ist ... # Was ist ...
        try:
            wikipedia.set_lang("de")
            return wikipedia.summary(i_thema, sentences=5)
        except Exception as e:
            return f"Ich weiss {i_thema} nicht"