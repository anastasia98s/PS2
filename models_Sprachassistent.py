from sqlalchemy import Column, Integer, String, ForeignKey, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from Base_CRUD import BaseCRUD
db_url = "sqlite:///db.db"
engine = create_engine(db_url)
Base = declarative_base()

class classifications(Base, BaseCRUD):
    __tablename__ = 'classification'
    id = Column(Integer, primary_key=True)
    Auswahl = Column(String, index=True)
    
    def __init__(self, Auswahl):
        self.Auswahl = Auswahl
    
    # 1:1 Beziehung zu intends  
    intend = relationship("intends", back_populates="classification", uselist=False)

class intends(Base, BaseCRUD):
    __tablename__ = 'intends'
    id = Column(Integer, primary_key=True)
    classification_id = Column(Integer, ForeignKey('classification.id'), unique=True)
    
    input_suchintend = Column(String, index=True, default = 'None')
    output_suchintend = Column(String, index=True, default = 'None')
    input_wikipedia = Column(String, index=True, default = 'None')
    output_wikipedia = Column(String, index=True, default = 'None')
    input_studienordnung = Column(String, index=True, default = 'None')
    output_studienordnung = Column(String, index=True, default = 'None')
    input_to_do_liste = Column(String, index=True, default = 'None')
    output_to_do_liste = Column(String, index=True, default = 'None')
    
    # 1:1 Beziehung zu classifications
    classification = relationship("classifications", back_populates="intend")


# Erstelle die Tabellen
Base.metadata.create_all(engine)