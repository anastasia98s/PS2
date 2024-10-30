from models_Sprachassistent import classifications, engine
from sqlalchemy.orm import sessionmaker

##################
### Read classifications
##################

def update_classifications(id):
    Session = sessionmaker(bind=engine)
    session = Session()
    
    # Abrufen aller Einträge in der classifications-Tabelle
    choosen_classification = session.query(classifications) \
                            .filter_by(id=id) \
                            .first()
                            
    aenderung = "Aus_dem_Herzen"
    choosen_classification.Auswahl = aenderung
    session.commit()
    return aenderung

if __name__ == "__main__":
    classification= update_classifications(1)
    print(classification)