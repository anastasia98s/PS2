import pdfplumber
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import requests

class StudienordnungIntent:
    def __init__(self):
        pass
    
    def convert_to_text(pdf):
        with pdfplumber.open(pdf) as pdf:
            all_text=""
            for page in pdf.pages:
                all_text+=page.extract_text() +"\n"
                all_text=remove_hyphenation(all_text)
            return all_text
    
    def remove_hyphenation(text):
        # Entfernt Bindestriche am Zeilenende und verbindet die getrennten Wörter
        # Beispiel: "Beispiel-\ntext" wird zu "Beispieltext"
        cleaned_text = re.sub(r'(\w+)-\n(\w+)', r'\1\2', text)
        
        # Optional: Entfernt auch alle weiteren Zeilenumbrüche, die keine Bindestriche haben
        cleaned_text = re.sub(r'\n', ' ', cleaned_text)  # Entfernt normale Zeilenumbrüche
        
        return cleaned_text

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
    

    # Funktion zur Relevanzbewertung und Auswahl der wichtigsten Chunks
    def get_top_relevant_chunks(paragraphs, question, top_n=2):
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

    # sends a prompt to the chat api
    def get_chat_response(model, prompt, url="http://localhost:11434/api/chat"):
        """
        Sendet eine Anfrage an den Chat-API-Endpunkt und gibt die Antwort zurück.
        
        :param model: Das Modell, das verwendet werden soll (z. B. "llama3.2").
        :param prompt: Die Eingabe des Benutzers, die gesendet werden soll.
        :param url: Der API-Endpunkt (standardmäßig auf localhost gesetzt).
        :return: Der Inhalt der Antwort vom Modell oder eine Fehlermeldung.
        """
        
        # Daten, die im Body der Anfrage gesendet werden sollen
        data = {
            "model": model,
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "stream": False
        }

        try:
            # Sende den POST-Request
            response = requests.post(url, json=data)

            # Überprüfe die Antwort
            if response.status_code == 200:
                response_data = response.json()  # Parse die JSON-Antwort
                # Extrahiere nur den Text aus der Antwort
                message_content = response_data["message"]["content"]
                return message_content
            else:
                return f"Fehler: {response.status_code} - {response.text}"

        except requests.exceptions.RequestException as e:
            return f"Ein Fehler ist aufgetreten: {e}"
        

    def get_aggregated_answer(chunks, question):
        all_answers = []
        
        for chunk in chunks:
            prompt = f"Lies den folgenden Text und beantworte die Frage nur auf Grundlage der bereitgestellten Informationen: {chunk} \n\nFrage: {question}"
            answer = get_chat_response("llama3.2", prompt)
            all_answers.append(answer)
        # Alle Antworten zusammenführen und eine aggregierte Antwort erstellen
        aggregated_answer = " ".join(all_answers)
        return aggregated_answer

    def abfragen(self, i_thema):
        # TODO
        """
            Wenn du zusätzliche Variablen benötigst, 
            kannst du selbstverständlich auch andere Variablen verwenden und nicht nur `i_thema`.
            Die Wahl der Variablen hängt von den Anforderungen und dem Kontext deines Projekts ab.
        """
        return f"{i_thema} bedeutet ....", None