from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine
from typing import List
from models import classifications, intends
from schemas import ClassificationSchema, IntendSchema
import uvicorn

# FastAPI-App erstellen
app = FastAPI()

# Datenbankverbindung einrichten
db_url = "sqlite:///input_output_analyse.db"
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
    new_classification = classifications(Auswahl=data.Auswahl)
    db.add(new_classification)
    db.commit()
    db.refresh(new_classification)
    return new_classification

@app.get("/classifications/{classification_id}", response_model=ClassificationSchema)
def get_classification_by_id(classification_id: int, db: SessionLocal = Depends(get_db)):
    classification = db.query(classifications).filter_by(id=classification_id).first()
    if not classification:
        raise HTTPException(status_code=404, detail="Classification not found")
    return classification

@app.put("/classifications/{classification_id}", response_model=ClassificationSchema)
def update_classification(classification_id: int, data: ClassificationSchema, db: SessionLocal = Depends(get_db)):
    classification = db.query(classifications).filter_by(id=classification_id).first()
    if not classification:
        raise HTTPException(status_code=404, detail="Classification not found")
    classification.Auswahl = data.Auswahl
    db.commit()
    db.refresh(classification)
    return classification

@app.delete("/classifications/{classification_id}")
def delete_classification(classification_id: int, db: SessionLocal = Depends(get_db)):
    classification = db.query(classifications).filter_by(id=classification_id).first()
    if not classification:
        raise HTTPException(status_code=404, detail="Classification not found")
    db.delete(classification)
    db.commit()
    return {"deleted": classification_id}

# CRUD-Endpunkte für Intends
@app.get("/intends", response_model=List[IntendSchema])
def get_intends(db: SessionLocal = Depends(get_db)):
    return db.query(intends).all()

@app.post("/intends", response_model=IntendSchema)
def create_intend(data: IntendSchema, db: SessionLocal = Depends(get_db)):
    new_intend = intends(
        classification_id=data.classification_id,
        input_suchintend=data.input_suchintend,
        output_suchintend=data.output_suchintend,
        input_wikipedia=data.input_wikipedia,
        output_wikipedia=data.output_wikipedia,
        input_studienordnung=data.input_studienordnung,
        output_studienordnung=data.output_studienordnung,
        input_to_do_liste=data.input_to_do_liste,
        output_to_do_liste=data.output_to_do_liste,
    )
    db.add(new_intend)
    db.commit()
    db.refresh(new_intend)
    return new_intend

@app.get("/intends/{intend_id}", response_model=IntendSchema)
def get_intend_by_id(intend_id: int, db: SessionLocal = Depends(get_db)):
    intend = db.query(intends).filter_by(id=intend_id).first()
    if not intend:
        raise HTTPException(status_code=404, detail="Intend not found")
    return intend

@app.put("/intends/{intend_id}", response_model=IntendSchema)
def update_intend(intend_id: int, data: IntendSchema, db: SessionLocal = Depends(get_db)):
    intend = db.query(intends).filter_by(id=intend_id).first()
    if not intend:
        raise HTTPException(status_code=404, detail="Intend not found")
    intend.classification_id = data.classification_id
    intend.input_suchintend = data.input_suchintend
    intend.output_suchintend = data.output_suchintend
    intend.input_wikipedia = data.input_wikipedia
    intend.output_wikipedia = data.output_wikipedia
    intend.input_studienordnung = data.input_studienordnung
    intend.output_studienordnung = data.output_studienordnung
    intend.input_to_do_liste = data.input_to_do_liste
    intend.output_to_do_liste = data.output_to_do_liste
    db.commit()
    db.refresh(intend)
    return intend

@app.delete("/intends/{intend_id}")
def delete_intend(intend_id: int, db: SessionLocal = Depends(get_db)):
    intend = db.query(intends).filter_by(id=intend_id).first()
    if not intend:
        raise HTTPException(status_code=404, detail="Intend not found")
    db.delete(intend)
    db.commit()
    return {"deleted": intend_id}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
