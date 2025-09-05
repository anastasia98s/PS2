from sqlalchemy.orm import sessionmaker
from models_Sprachassistent import classifications, engine 




##################
# CREATE classification 
##################
def save_classification(Auswahl):
    Session = sessionmaker(bind=engine)

    session = Session()
    
    # classificationsobjekt anlegen. 
    auswahl= classifications(Auswahl)


    # Userobjekte zur Datenbank hinzufügen. 
    session.add(auswahl) 
    # session.add_all([auswahl_1, auswahl_2])

    session.commit()
    
if __name__== "__main__":
    save_classification("suchindent")
    