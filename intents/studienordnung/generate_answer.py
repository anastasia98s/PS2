from langchain_ollama import OllamaLLM
import config

def get_aggregated_answer(chunks, question):
    all_answers = []
    for chunk in chunks:
        prompt = f"Lies den folgenden Text und beantworte die Frage kurz und nur auf Grundlage der bereitgestellten Informationen: {chunk} \n\nFrage: {question}"
        answer = get_chat_response(config.STUDIENORDNUNG_OLLAMA_MODELL, prompt)
        all_answers.append(answer)
    
    # Alle Antworten zusammenführen und eine aggregierte Antwort erstellen
    aggregated_answer = " ".join(all_answers)
    return aggregated_answer

def get_chat_response(model, prompt):
    """
    Sendet eine Anfrage an den Chat-API-Endpunkt und gibt die Antwort zurück.
    
    :param model: Das Modell, das verwendet werden soll (z. B. "llama3.2").
    :param prompt: Die Eingabe des Benutzers, die gesendet werden soll.
    :param url: Der API-Endpunkt (standardmäßig auf localhost gesetzt).
    :return: Der Inhalt der Antwort vom Modell oder eine Fehlermeldung.
    """
    
    # Daten, die im Body der Anfrage gesendet werden sollen
    model = OllamaLLM(model=model) 
    return model(prompt)