from datetime import date

from sklearn.metrics.pairwise import cosine_similarity
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import normalize

from dbbind import Session, User
from todo import ToDoList
from tts import speak, listen, record_audio, extract_features
import numpy as np

# Mapping German numbers to integers
text_to_number = {
    "eins": 1,
    "zwei": 2,
    "drei": 3,
    "vier": 4,
    "fünf": 5,
    "sechs": 6,
    "sieben": 7,
    "acht": 8,
    "neun": 9,
    "zehn": 10
}


def identify_user(features, session, model=None):
    """Identify the user based on the extracted audio features."""
    users = session.query(User).all()

    # Normalize the input features
    features = normalize(features.reshape(1, -1)).flatten()

    # Prepare stored features and labels for the model
    stored_features = []
    labels = []

    for user in users:
        if user.audio_features is not None:
            # Assuming user.audio_features is a bytes object that can be converted to numpy array
            user_features = np.frombuffer(user.audio_features, dtype=np.float32)
            stored_features.append(user_features)
            labels.append(user.id)  # Assuming user.id is the identifier

    if not stored_features:
        return None  # No users to compare

    # Convert to numpy array and normalize
    stored_features = np.array(stored_features)
    stored_features = normalize(stored_features)

    if model is None:
        # If no model is provided, use k-NN as a fallback
        model = NearestNeighbors(n_neighbors=1, metric='cosine')
        model.fit(stored_features)

    # Find the closest user
    distances, indices = model.kneighbors(features.reshape(1, -1))

    # Check if the closest user is within an acceptable distance threshold
    if distances[0][0] < 0.1:  # Example threshold, adjust as necessary
        closest_user_id = labels[indices[0][0]]
        closest_user = session.query(User).filter_by(id=closest_user_id).first()
        return closest_user
    else:
        return None  # No close match found

def main():
    session = Session()
    speak("Hi What i can help you")

    audio_filename = "user_voice.wav"
    record_audio(audio_filename)  # Record the user's voice

    # Extract audio features
    features = extract_features(audio_filename)


        # Identify the user based on recorded features
    user = identify_user(features, session)
    speak("Wait")

    if user:
        speak(f"Willkommen zurück, {user.name}!")
    else:
        speak("Ich konnte Sie nicht identifizieren. Bitte sagen Sie Ihren Namen.")
        user_name = listen()
        if user_name:
            user_name = user_name.lower()
            # Create a new user if not identified
            new_user = User(name=user_name, audio_features=features.tobytes())
            session.add(new_user)
            session.commit()
            speak(f"Willkommen, {user_name}! Sie wurden als neuer Benutzer hinzugefügt.")

    # Main loop for task management
    todo = ToDoList(user_id=user.id if user else None)  # Set user ID if identified

    speak("Hallo! Ich bin Ihr Assistent. Sie können mir sagen, was ich tun soll.")

    while True:
        print("\nOptionen:")
        print("1. Neue Aufgabe")
        print("2. Aufgaben anzeigen")
        print("3. Aufgabe löschen")
        print("4. Beenden")

        command = listen()  # Listen for a command
        if command:

            command = command.lower()
            if "beenden" in command:
                speak("Auf Wiedersehen!")
                break
            elif "neue aufgabe" in command:
                speak("Was ist die Aufgabe, die Sie hinzufügen möchten?")
                task = listen()
                if task:
                    due_date = date.today().isoformat()   # Set due date to today
                    todo.add_task(task, due_date)
                else:
                    speak("Ich habe die Aufgabe nicht verstanden. Bitte versuchen Sie es erneut.")
            elif "aufgaben anzeigen" in command:
                todo.view_tasks()  # Display tasks in the console
                todo.speak_tasks()  # Speak tasks if requested
            elif "aufgabe löschen" in command:
                speak("Bitte sagen Sie mir die Nummer der Aufgabe, die entfernt werden soll.")
                task_number = listen()
                print(task_number)

                # Convert spoken number to integer
                if task_number in text_to_number:
                    task_number = text_to_number[task_number]
                else:
                    try:
                        task_number = int(task_number)  # Try converting to integer directly
                    except (ValueError, TypeError):
                        speak("Bitte sagen Sie eine gültige Aufgabennummer.")
                        continue  # Skip the rest of the loop if conversion fails

                # Remove the task if the number is valid
                if task_number is not None and task_number > 0:
                    try:
                        todo.remove_task(task_number)
                    except IndexError:
                        speak("Die Aufgabennummer existiert nicht. Bitte versuchen Sie es erneut.")
                else:
                    speak("Bitte sagen Sie eine gültige Aufgabennummer.")
            else:
                speak("Ich habe diesen Befehl nicht verstanden. Bitte versuchen Sie es erneut.")
        else:
            speak("Bitte versuchen Sie es erneut.")

    todo.close()  # Close the session when done

if __name__ == "__main__":
    main()