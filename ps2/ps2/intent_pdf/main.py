from pdf_to_text_converter import convert_to_text
from ps2.ps2.Sprachassistent.intent_pdf.text_into_paragraphs import split_text_into_paragraphs
from identify_relevant_chunks import get_top_relevant_chunks
from generate_answer import get_aggregated_answer


def main():
    # path to PDF with Prüfungsordnung
    pdf_path = "I42b_2010_PO.pdf"
    question=input("Geben Sie eine Frage ein:")

    pdf_text=convert_to_text(pdf_path)
    chunks=split_text_into_paragraphs(pdf_text)

    paragraphs=get_top_relevant_chunks(chunks, question)

        # # Ausgabe der Chunks zur Überprüfung
    # for i, paragraph in enumerate(paragraphs):
    #     print(f"Chunk {i + 1}:\n{paragraph[:200]}...\n")  # Zeigt die ersten 200 Zeichen jedes Chunks

    final_answer=get_aggregated_answer(paragraphs, question)

    print("Antwort: ")
    print(final_answer)

if __name__=="__main__":
    main()