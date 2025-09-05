from datetime import datetime
from tts import speak  # Assuming you have a text-to-speech module
from sqlalchemy.exc import IntegrityError
from dbbind import User, Task, Session  # Ensure correct import of Session

class ToDoList:
    def __init__(self, user_id=1):
        self.user_id = user_id
        self.session = Session()

    def ensure_user_exists(self):
        # Check if the user already exists
        user = self.session.query(User).filter_by(id=self.user_id).first()
        if not user:
            # If the user does not exist, create it
            new_user = User(id=self.user_id, name="Nuha")
            self.session.add(new_user)
            try:
                self.session.commit()
            except IntegrityError:
                self.session.rollback()  # Rollback in case of error
                print("User  already exists or another integrity error occurred.")
        speak(f"Welcome  '{user.name}' ")

    def add_task(self, task_description, due_date):
        new_task = Task(user_id=self.user_id, task=task_description, due_date=due_date)
        self.session.add(new_task)
        try:
            self.session.commit()
            speak(f"Aufgabe '{task_description}' hinzugefügt mit Fälligkeitsdatum {due_date}.")
        except IntegrityError:
            self.session.rollback()
            speak("Fehler beim Hinzufügen der Aufgabe.")

    def view_tasks(self):
        tasks = self.session.query(Task).filter(Task.user_id == self.user_id).all()
        for i, task in enumerate(tasks, start=1):
            print(f"{i}. {task.task} (Fälligkeitsdatum: {task.due_date})")

    def speak_tasks(self):
        tasks = self.session.query(Task).filter(Task.user_id == self.user_id).all()
        if not tasks:
            speak("Sie haben keine Aufgaben.")
        else:
            speak("Hier sind Ihre Aufgaben:")
            for i, task in enumerate(tasks, start=1):
                speak(f"{i}. {task.task} (Fälligkeitsdatum: {task.due_date})")

    def remove_task(self, task_number):
        tasks = self.session.query(Task).filter(Task.user_id == self.user_id).all()
        try:
            task_to_remove = tasks[task_number - 1]
            self.session.delete(task_to_remove)
            self.session.commit()
            speak(f"Aufgabe '{task_to_remove.task}' entfernt.")
        except IndexError:
            speak("Bitte sagen Sie eine gültige Aufgabennummer.")
        except Exception as e:
            self.session.rollback()
            speak("Fehler beim Entfernen der Aufgabe.")

    def close(self):
        self.session.close()