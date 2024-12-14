import api
from fastapi import FastAPI
from typing import Dict, Any
import uvicorn
import wikipedia
import logging
from langchain_ollama import OllamaLLM
import config

# Logger konfigurieren
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

wikipedia.set_lang("de")

app = FastAPI()

def ollama_fragen(information, question):
    if not information or not question:
        return "Wikipedia-Fehler"

    prompt = f"Informationen: {information} \n\nFrage: {question}. Beantworte die Frage so kurz wie möglich anhand der Informationen."
    model = OllamaLLM(model=config.STUDIENORDNUNG_OLLAMA_MODELL) 
    return model(prompt)

@app.post("/wikipedia_intent/abfragen") 
def abfragen(item: Dict[Any, Any]):
    i_satz = item.get("satz")
    i_thema = item.get("thema")
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
        ollama_antwort = ollama_fragen(summary, i_satz)
        return ollama_antwort, None
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