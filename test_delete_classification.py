from models_Sprachassistent import classifications, engine
from sqlalchemy.orm import sessionmaker, delete

##################
### Read classifications
##################

def update_classifications(id):
    Session = sessionmaker(bind=engine)
    session = Session()
    
    # Abrufen aller Einträge in der classifications-Tabelle
    choosen_classification = session.query(classifications) \
                            .filter_by(id=id) \
                            .one_or_none()
                            
    choosen_classification.delete()
    session.commit()
    return 0

if __name__ == "__main__":
    classification= update_classifications(1)
    print(classification)