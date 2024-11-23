import wikipedia
import logging
import config

# Logger konfigurieren
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

class WikipediaIntent:
    def __init__(self, text_to_speech):
        self.text_to_speech = text_to_speech
        wikipedia.set_lang("de")
    
    def abfragen(self, i_thema):
        """
        Ruft eine kurze Zusammenfassung eines Wikipedia-Artikels ab.

        :param i_thema: Das Thema, zu dem Informationen abgefragt werden sollen.
        :return: Eine kurze Zusammenfassung des Wikipedia-Artikels oder eine Fehlermeldung.
        """

        if not i_thema:
            return None, config.ERROR_VARIABLE_THEMA # frage nochmal zum Thema
        
        self.text_to_speech.text_to_speech(f"Moment, suche nach {i_thema} in Wikipedia")
        
        logger.info(f"Wikipedia Intent aufgerufen. Thema: '{i_thema}'")
        
        try:
            # Wikipedia-Zusammenfassung für das angegebene Thema holen
            summary = wikipedia.summary(i_thema, sentences=5)
            logger.info("Zusammenfassung erfolgreich abgerufen.")
            return summary, None
        except wikipedia.DisambiguationError as e:
            logger.warning(f"Mehrdeutigkeit festgestellt: {e.options}")
            return f"Das Thema '{i_thema}' ist mehrdeutig. Versuche es spezifischer zu formulieren.", None
        except wikipedia.PageError:
            logger.error(f"Kein Artikel gefunden für das Thema: '{i_thema}'")
            return f"Es wurde kein Wikipedia-Artikel für das Thema '{i_thema}' gefunden.", None
        except Exception as e:
            logger.exception("Ein unerwarteter Fehler ist aufgetreten.")
            return "Ein Fehler ist aufgetreten. Bitte versuche es erneut.", None
        
""" # Testen des Wikipedia-Intents
if __name__ == "__main__":
    intent = WikipediaIntent()
    thema = "Künstliche Intelligenz"
    zusammenfassung, fehler = intent.abfragen(thema)
    
    if fehler:
        print(f"Fehler: {fehler}")
    else:
        print(f"Zusammenfassung:\n{zusammenfassung}") """