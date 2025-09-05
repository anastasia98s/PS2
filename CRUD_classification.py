from sqlalchemy.orm import sessionmaker
import sys
import os
# Zum übergeordneten Verzeichnis hinzufügen
sys.path.append(os.path.abspath(".."))
from models_Sprachassistent import  engine, classifications

Session = sessionmaker(bind=engine)

session = Session()

# 1. Ein neues Objekt erstellen
# new_classification = classifications.create(session, Auswahl="Beispielwahl")

# 2. Ein Objekt lesen
classification = classifications.read_one(session, id=1)

# 3. Alle Objekte mit einem bestimmten Filter lesen
classifications_all = classifications.read(session, Auswahl="Beispielwahl")
print(classifications_all)
# 4. Ein Objekt aktualisieren
updated_classification = classifications.update(session, 1, Auswahl="Neue Wahl")

# 5. Ein Objekt löschen
deleted = classifications.delete(session, 1)

# Session schließen
session.close()