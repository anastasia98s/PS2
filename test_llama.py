import requests
import json

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

if __name__=='__main__':
    # Beispiel-Aufruf der Funktion
    antwort = get_chat_response("llama3.2", "Why is the sky blue?")
    print("Antwort:", antwort)