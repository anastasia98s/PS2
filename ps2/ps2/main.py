from datetime import date
from todo import ToDoList
from tts import speak, listen


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

def main():
    todo = ToDoList()



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
                todo.view_tasks()  # This will display tasks in the console
                todo.speak_tasks()  # This will speak tasks if requested
            elif "aufgabe löschen" in command:
                speak("Bitte sagen e Sie mir die Nummer der Aufgabe, die entfernt werden soll.")
                task_number = listen()
                print(task_number)

                if task_number in text_to_number:
                    task_number = text_to_number[task_number]
                else:
                    try:
                        task_number = int(task_number)  # Try converting to integer directly
                    except (ValueError, TypeError):
                        speak("Bitte sagen Sie eine gültige Aufgabennummer.")
                        continue  # Skip the rest of the loop if conversion fails
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


if __name__ == "__main__":
    main()