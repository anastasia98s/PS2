from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Funktion zur Relevanzbewertung und Auswahl der wichtigsten Chunks
def get_top_relevant_chunks(paragraphs, question, top_n=1):
    # Erstelle TF-IDF Vektoren für die Paragraphen und die Frage
    vectorizer = TfidfVectorizer().fit(paragraphs + [question])
    paragraph_vectors = vectorizer.transform(paragraphs)
    question_vector = vectorizer.transform([question])
    
    # Berechne die Kosinus-Ähnlichkeit zwischen der Frage und jedem Paragraphen
    similarities = cosine_similarity(paragraph_vectors, question_vector).flatten()
    
    # Sortiere Paragraphen basierend auf Relevanz und wähle die Top N aus
    top_indices = similarities.argsort()[-top_n:][::-1]
    top_paragraphs = [paragraphs[i] for i in top_indices]
    
    return top_paragraphs