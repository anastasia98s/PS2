import wikipedia
import logging

# Logger konfigurieren
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

class WikipediaIntent:
    def __init__(self):
        """
        Initialisiert den WikipediaIntent. Kann später erweitert werden, falls Konfigurationen nötig sind.
        """
        # Standard-Einstellung für Wikipedia-Sprache
        wikipedia.set_lang("de")

    def abfragen(self, i_thema):
        """
        Ruft eine kurze Zusammenfassung eines Wikipedia-Artikels ab.

        :param i_thema: Das Thema, zu dem Informationen abgefragt werden sollen.
        :return: Eine kurze Zusammenfassung des Wikipedia-Artikels oder eine Fehlermeldung.
        """
        
        logger.info(f"Wikipedia Intent aufgerufen. Thema: '{i_thema}'")
        
        try:
            # Wikipedia-Zusammenfassung für das angegebene Thema holen
            summary = wikipedia.summary(i_thema, sentences=5)
            logger.info("Zusammenfassung erfolgreich abgerufen.")
            return summary, None
        except wikipedia.DisambiguationError as e:
            logger.warning(f"Mehrdeutigkeit festgestellt: {e.options}")
            return None, f"Das Thema '{i_thema}' ist mehrdeutig. Versuche es spezifischer zu formulieren."
        except wikipedia.PageError:
            logger.error(f"Kein Artikel gefunden für das Thema: '{i_thema}'")
            return None, f"Es wurde kein Wikipedia-Artikel für das Thema '{i_thema}' gefunden."
        except Exception as e:
            logger.exception("Ein unerwarteter Fehler ist aufgetreten.")
            return None, "Ein Fehler ist aufgetreten. Bitte versuche es erneut."

# Testen des Wikipedia-Intents
if __name__ == "__main__":
    intent = WikipediaIntent()
    thema = "Künstliche Intelligenz"
    zusammenfassung, fehler = intent.abfragen(thema)
    
    if fehler:
        print(f"Fehler: {fehler}")
    else:
        print(f"Zusammenfassung:\n{zusammenfassung}")
