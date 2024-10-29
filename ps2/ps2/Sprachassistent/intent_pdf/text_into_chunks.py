import re


# splits text into paragraphs for better context
def split_text_into_paragraphs(text, max_chunk_size=1024):
    # Split the text into sections based on paragraph markers (e.g., §)
    paragraphs = re.split(r'(§\s?\d+)', text)  # Teilung anhand der Paragraphenmarker
    chunks = []
    current_chunk = ""
    
    # Hier fügen wir die Paragraphen zusammen und überprüfen die Länge
    for i in range(1, len(paragraphs), 2):  # Indizes für Paragraphen
        paragraph_number = paragraphs[i].strip()  # Paragraphen-Nummer
        paragraph_content = paragraphs[i + 1].strip() if i + 1 < len(paragraphs) else ""

        # Wenn der aktuelle Chunk nicht leer ist und das Hinzufügen des Paragraphen den Chunk zu groß macht
        if current_chunk and (len(current_chunk) + len(paragraph_number) + len(paragraph_content) > max_chunk_size):
            chunks.append(current_chunk.strip())  # Chunk hinzufügen
            current_chunk = paragraph_number + " " + paragraph_content  # Neuen Chunk beginnen
        else:
            # Füge den Paragraphen zum aktuellen Chunk hinzu
            current_chunk += " " + paragraph_number + " " + paragraph_content
    
    # Füge den letzten Chunk hinzu, falls vorhanden
    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks



# Tokenizer, der den Text in Wörter aufteilt
def tokenize(text):
    tokens = re.findall(r'\w+|\S', text)  # Wörter und Sonderzeichen erfassen
    return tokens


# Funktion, um den Text in Sätze aufzuteilen
def split_into_sentences(text):
    # Aufteilung basierend auf Punktuation (., !, ?)
    sentences = re.split(r'(?<=[.!?]) +', text)
    return sentences


# splits text in tokens and minds sentence structure for better context
def split_text_by_tokens(text, max_tokens=512):

    # In Sätze aufteilen
    sentences = split_into_sentences(text)
    chunks = []
    current_chunk = []
    current_token_count = 0

    for sentence in sentences:
        # Tokenize den Satz
        sentence_tokens = tokenize(sentence)
        sentence_token_count = len(sentence_tokens)

        # Wenn der aktuelle Chunk mit diesem Satz zu groß wird, speichere den Chunk
        if current_token_count + sentence_token_count > max_tokens:
            chunks.append(" ".join(current_chunk))  # Chunk wieder in Textstring umwandeln
            current_chunk = []
            current_token_count = 0

        # Füge den aktuellen Satz zum Chunk hinzu
        current_chunk.append(sentence)
        current_token_count += sentence_token_count

    # Füge den letzten Chunk hinzu, falls noch Sätze übrig sind
    if current_chunk:
        chunks.append(" ".join(current_chunk))

    return chunks
