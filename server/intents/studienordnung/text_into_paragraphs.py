import re

def split_text_into_paragraphs(text, max_chunk_size=512):

    # Splitte anhand von Paragraphenmarkern
    paragraphs = re.split(r'(§\s?\d+)', text)
    combined_paragraphs = []
    current_chunk = ""
    last_paragraph = ""  # Speichert den letzten tatsächlichen Paragraphen

    for i in range(1, len(paragraphs), 2):  # Nur Paragraphenmarkierungen verarbeiten
        paragraph_number = paragraphs[i].strip()
        paragraph_content = paragraphs[i + 1].strip() if i + 1 < len(paragraphs) else ""

        # Prüfen, ob der aktuelle Paragraph eine Referenz ist
        if re.search(r"siehe\s*§|gemäß\s*§|nach\s*§|gem.\s*§|entsprechend\s*§", paragraph_content.lower()):
            # Falls es eine Referenz ist, füge sie zum letzten tatsächlichen Paragraphen hinzu
            if last_paragraph:
                last_paragraph += f" {paragraph_number} {paragraph_content}"
            continue  # Nicht als eigenständigen Chunk speichern
        else:
            # Ein echter Paragraph: vorherigen Chunk abschließen, wenn er zu groß wird
            if current_chunk and (len(current_chunk) + len(paragraph_number) + len(paragraph_content) > max_chunk_size):
                combined_paragraphs.append(current_chunk.strip())
                current_chunk = ""

            # Füge den aktuellen Paragraphen dem Chunk hinzu
            current_chunk += f" {paragraph_number} {paragraph_content}"
            last_paragraph = f"{paragraph_number} {paragraph_content}"  # Speichere für Referenzen

    # Letzten Chunk hinzufügen
    if current_chunk:
        combined_paragraphs.append(current_chunk.strip())

    return combined_paragraphs