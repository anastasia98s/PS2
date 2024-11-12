# Voice-Activated Task Management Assistant

## Overview
This project is a voice-activated task management assistant that identifies users based on their voice features and allows them to manage their tasks through voice commands. It utilizes audio feature extraction, voice recognition, and a simple task management system to provide an interactive experience.

## Features
- **User  Identification**: The assistant identifies users based on their unique voice features.
- **Task Management**: Users can add, view, and delete tasks using voice commands.
- **Voice Interaction**: The assistant communicates with users through speech synthesis and listens for commands.

## Requirements
- Python 3.x
- Required libraries:
  - `scikit-learn`
  - `numpy`
  - `dbbind` (for database interactions)
  - `todo` (for task management functionalities)
  - `tts` (for text-to-speech functionalities)

## Setup
1. **Install Dependencies**: Create a `requirements.txt` file with the following contents:
    ```
    scikit-learn
    numpy
    dbbind
    todo
    tts
    ```
   
   Then, install the required libraries using pip:
   ```bash
   pip install -r requirements.txt
   
2.Database Setup: Ensure that you have a database set up with a User  model and a session management system (Session).

3.Audio Features: The audio features for each user should be stored in the database in a format that can be converted to a numpy array.
4.Audio Recording: The system records user audio and extracts features from it.



## Usage

### Run the Script
To start the assistant, run the following command in your terminal:

```bash
python your_script_name.py
```
### Interaction:

The assistant will greet the user and prompt them to speak.
Users can say commands such as:
#### Add a New Task:
Say: "Neue Aufgabe, ich muss die Wäsche machen."
#### View Tasks:
Say: "Aufgaben anzeigen."
#### Delete a Task:
Say: "Aufgabe löschen, Nummer eins."
#### Exit the Assistant:
Say: "Beenden."

## Example Commands

### Adding a Task:
"Neue Aufgabe, ich muss die Wäsche machen."
### Viewing Tasks: 
"Aufgaben anzeigen."
### Deleting a Task: 
"Aufgabe löschen, Nummer eins."
###  Exiting:
"Beenden."