from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine
from typing import List
from models import classifications, YoutubeIntend, wikipedia_intends, studienordnung_intends, todo_intends
from schemas import (
    ClassificationSchema,
    IntendSchema,
    WikipediaIntendSchema,
    StudienordnungIntendSchema,
    TodoIntendSchema,
    ClassificationType
)
import uvicorn

# FastAPI-App erstellen
app = FastAPI()

# Datenbankverbindung einrichten
db_url = "sqlite:///test.db"
engine = create_engine(db_url, connect_args={"check_same_thread": False})
SessionLocal = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))


# Hilfsfunktion: Datenbank-Sitzung abrufen
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# CRUD-Endpunkte für Classifications
@app.get("/classifications", response_model=List[ClassificationSchema])
def get_classifications(db: SessionLocal = Depends(get_db)):
    return db.query(classifications).all()


@app.post("/classifications", response_model=ClassificationSchema)
def create_classification(data: ClassificationSchema, db: SessionLocal = Depends(get_db)):
    # Überprüfe, ob die Auswahl ein gültiger Typ ist
    if data.Auswahl not in ClassificationType:
        raise HTTPException(status_code=400, detail="Invalid classification type provided.")
    
    # Klassifikation erstellen
    new_classification = classifications(Auswahl=data.Auswahl.value)  # .value, um den String-Wert aus Enum zu bekommen
    db.add(new_classification)
    db.commit()
    db.refresh(new_classification)
    return ClassificationSchema(id=new_classification.id, Auswahl=new_classification.Auswahl)



# CRUD-Endpunkte für YoutubeIntend
@app.get("/youtube-intend", response_model=List[IntendSchema])
def get_youtube_intends(db: SessionLocal = Depends(get_db)):
    return db.query(YoutubeIntend).all()


@app.post("/youtube-intend", response_model=IntendSchema)
def create_youtube_intend(data: IntendSchema, db: SessionLocal = Depends(get_db)):
    new_intend = YoutubeIntend(
        classification_id=data.classification_id,
        input_YoutubeIntend=data.input_YoutubeIntend,
        output_YoutubeIntend=data.output_YoutubeIntend,
    )
    db.add(new_intend)
    db.commit()
    db.refresh(new_intend)
    return new_intend


# CRUD-Endpunkte für Wikipedia Intends
@app.get("/wikipedia-intend", response_model=List[WikipediaIntendSchema])
def get_wikipedia_intends(db: SessionLocal = Depends(get_db)):
    return db.query(wikipedia_intends).all()


@app.post("/wikipedia-intend", response_model=WikipediaIntendSchema)
def create_wikipedia_intend(data: WikipediaIntendSchema, db: SessionLocal = Depends(get_db)):
    new_wikipedia_intend = wikipedia_intends(
        classification_id=data.classification_id,
        input_wikipedia=data.input_wikipedia,
        output_wikipedia=data.output_wikipedia,
    )
    db.add(new_wikipedia_intend)
    db.commit()
    db.refresh(new_wikipedia_intend)
    return new_wikipedia_intend


# Ähnliche Routen für Studienordnung und To-Do-Listen
@app.get("/studienordnung-intend", response_model=List[StudienordnungIntendSchema])
def get_studienordnung_intends(db: SessionLocal = Depends(get_db)):
    return db.query(studienordnung_intends).all()


@app.post("/studienordnung-intend", response_model=StudienordnungIntendSchema)
def create_studienordnung_intend(data: StudienordnungIntendSchema, db: SessionLocal = Depends(get_db)):
    new_studienordnung_intend = studienordnung_intends(
        classification_id=data.classification_id,
        input_studienordnung=data.input_studienordnung,
        output_studienordnung=data.output_studienordnung,
    )
    db.add(new_studienordnung_intend)
    db.commit()
    db.refresh(new_studienordnung_intend)
    return new_studienordnung_intend


@app.get("/todo-intend", response_model=List[TodoIntendSchema])
def get_todo_intends(db: SessionLocal = Depends(get_db)):
    return db.query(todo_intends).all()


@app.post("/todo-intends", response_model=TodoIntendSchema)
def create_todo_intend(data: TodoIntendSchema, db: SessionLocal = Depends(get_db)):
    new_todo_intend = todo_intends(
        classification_id=data.classification_id,
        input_to_do_liste=data.input_to_do_liste,
        output_to_do_liste=data.output_to_do_liste,
    )
    db.add(new_todo_intend)
    db.commit()
    db.refresh(new_todo_intend)
    return new_todo_intend


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
