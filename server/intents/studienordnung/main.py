import api
from fastapi import FastAPI, Body
import uvicorn

from pdf_to_text_converter import convert_to_text
from text_into_paragraphs import split_text_into_paragraphs
from identify_relevant_chunks import get_top_relevant_chunks
from generate_answer import get_aggregated_answer
import config

app = FastAPI()

@app.post("/studienordnung_intent/abfragen") 
def abfragen(i_satz: str = Body(...)):
    try:
        pdf_text = convert_to_text(config.STUDIENORDNUNG_PDF_PATH)
        chunks = split_text_into_paragraphs(pdf_text)
        paragraphs = get_top_relevant_chunks(chunks, i_satz)
        final_answer = get_aggregated_answer(paragraphs, i_satz)

        return final_answer, None
    except FileNotFoundError:
        return "Studienordnung-PDF wurde nicht gefunden.", None
    except Exception as e:
        return "Fehler bei Ollama", None
    
if __name__ == "__main__":
    uvicorn.run("main:app", host=api.STUDIENORDNUNG_INTENT_SERVICE_IP, port=api.STUDIENORDNUNG_INTENT_SERVICE_PORT)