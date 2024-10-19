import json
from datetime import datetime

from tts import speak


class ToDoList:
    def __init__(self, filename='tasks.json'):
        self.tasks = []
        self.filename = filename
        self.load_tasks()

    def add_task(self, task, due_date):
        self.tasks.append({'task': task, 'due_date': due_date})
        self.save_tasks()
        speak(f"Aufgabe '{task}' hinzugefügt mit Fälligkeitsdatum {due_date}.")

    def view_tasks(self):
        for i, task in enumerate(self.tasks, start=1):
            print(f"{i}. {task['task']} (Fälligkeitsdatum: {task['due_date']})")

    def speak_tasks(self):
        if not self.tasks:
            speak("Sie haben keine Aufgaben.")
        else:
            speak("Hier sind Ihre Aufgaben:")
            for i, task in enumerate(self.tasks, start=1):
                speak(f"{i}. {task['task']} (Fälligkeitsdatum: {task['due_date']})")

    def remove_task(self, task_number):
        try:
            del self.tasks[task_number - 1]
            self.save_tasks()
        except IndexError:
            speak("Bitte sagen Sie eine gültige Aufgabennummer.")

    def save_tasks(self):
        with open(self.filename, 'w') as file:
            json.dump(self.tasks, file)

    def load_tasks(self):
        try:
            with open(self.filename, 'r') as file:
                content = file.read()
                if content:  # Only load if content is not empty
                    self.tasks = json.loads(content)
                else:
                    self.tasks = []
        except FileNotFoundError:
            self.tasks = []
        except json.JSONDecodeError:
            print("Warning: The tasks file is corrupted or empty. Starting with an empty task list.")
            self.tasks = []