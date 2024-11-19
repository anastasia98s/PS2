from intents.studienordnung.pdf_to_text_converter import convert_to_text
from intents.studienordnung.text_into_paragraphs import split_text_into_paragraphs
from intents.studienordnung.identify_relevant_chunks import get_top_relevant_chunks
from intents.studienordnung.generate_answer import get_aggregated_answer
import config

class StudienordnungIntent:
    def __init__(self, processor_class_engine):
        self.processor_class_engine = processor_class_engine
    
    def abfragen(self, i_satz):
        if self.processor_class_engine.thread_event.is_set():
            return None, None
        
        pdf_text = convert_to_text(config.STUDIENORDNUNG_PDF_PATH)
        chunks = split_text_into_paragraphs(pdf_text)
        paragraphs = get_top_relevant_chunks(chunks, i_satz)
        final_answer = get_aggregated_answer(paragraphs, i_satz)

        return final_answer, None