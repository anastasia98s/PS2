from models_Sprachassistent import classifications, engine
from sqlalchemy.orm import sessionmaker

##################
### Read classifications
##################

def read_all_classifications():
    Session = sessionmaker(bind=engine)
    session = Session()
    
    # Abrufen aller Einträge in der classifications-Tabelle
    all_classifications = session.query(classifications).all()
    
    return all_classifications

if __name__ == "__main__":
    classification= read_all_classifications()
    print(classification[0].Auswahl)