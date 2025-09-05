from sqlalchemy.orm import sessionmaker
import sys
import os
# Zum übergeordneten Verzeichnis hinzufügen
sys.path.append(os.path.abspath(".."))
from models_Sprachassistent import intends, engine

Session = sessionmaker(bind=engine)

session = Session()

# 1. Ein neues Objekt erstellen
new_intend = intends.create(
    session,
    classification_id=1,  # Beispiel-Classification-ID
    input_suchintend="Beispiel Suchintention",
    output_suchintend="Beispiel Antwort",
    input_wikipedia="Beispiel Wikipedia Anfrage",
    output_wikipedia="Beispiel Wikipedia Antwort",
    input_studienordnung="Beispiel Studienordnung Anfrage",
    output_studienordnung="Beispiel Studienordnung Antwort",
    input_to_do_liste="Beispiel To-Do Anfrage",
    output_to_do_liste="Beispiel To-Do Antwort"
)
print("Neues Intent erstellt:", new_intend)

# 2. Ein einzelnes Objekt lesen (mit `id=1` als Beispiel)
intend_instance = intends.read_one(session, id=1)
print("Gelesenes Intent:", intend_instance)

# 3. Alle Objekte mit einem bestimmten Filter lesen
intends_all = intends.read(session, input_suchintend="Beispiel Suchintention")
print("Gefilterte Intents:", intends_all)

# 4. Ein Objekt aktualisieren
'''
updated_intend = intends.update(
    session, 
    id=1,  # Beispiel-ID
    output_suchintend="Aktualisierte Antwort",
    input_to_do_liste="Aktualisierte To-Do Anfrage"
)
print("Aktualisiertes Intent:", updated_intend)
'''


# 5. Ein Objekt löschen
# deleted = intends.delete(session, id=1)
# print("Intent gelöscht:", deleted)

# Session schließen
session.close()