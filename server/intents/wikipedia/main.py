import api
from fastapi import FastAPI, Body
import uvicorn
import wikipedia
import logging

# Logger konfigurieren
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

wikipedia.set_lang("de")

app = FastAPI()

@app.post("/wikipedia_intent/abfragen") 
def abfragen(i_thema: str = Body(...)):
    """
    Ruft eine kurze Zusammenfassung eines Wikipedia-Artikels ab.

    :param i_thema: Das Thema, zu dem Informationen abgefragt werden sollen.
    :return: Eine kurze Zusammenfassung des Wikipedia-Artikels oder eine Fehlermeldung.
    """

    if not i_thema:
        return None, api.ERROR_VARIABLE_THEMA # frage nochmal zum Thema
    
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
    
if __name__ == "__main__":
    uvicorn.run("main:app", host=api.WIKIPEDIA_INTENT_SERVICE_IP, port=api.WIKIPEDIA_INTENT_SERVICE_PORT)