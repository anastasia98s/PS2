from get_llama_answer import get_chat_response

def get_aggregated_answer(chunks, question):
    all_answers = []
    for chunk in chunks:
        prompt = f"Lies den folgenden Text und beantworte die Frage nur auf Grundlage der bereitgestellten Informationen: {chunk} \n\nFrage: {question}"
        answer = get_chat_response("llama3.2", prompt)
        all_answers.append(answer)
    
    # Alle Antworten zusammenführen und eine aggregierte Antwort erstellen
    aggregated_answer = " ".join(all_answers)
    return aggregated_answer