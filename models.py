from sqlalchemy import Column, Integer, String, ForeignKey, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from Base_CRUD import BaseCRUD

db_url = "sqlite:///test.db"
engine = create_engine(db_url)
Base = declarative_base()

# SQLAlchemy-Modelle
class classifications(Base, BaseCRUD):
    __tablename__ = 'classification'
    id = Column(Integer, primary_key=True)
    Auswahl = Column(String, index=True)

    def __init__(self, Auswahl):
        self.Auswahl = Auswahl

    # 1:n Beziehung zu Intends
    intends = relationship("YoutubeIntend", back_populates="classification")


class YoutubeIntend(Base, BaseCRUD):
    __tablename__ = 'youtube_intends'
    id = Column(Integer, primary_key=True)
    classification_id = Column(Integer, ForeignKey('classification.id'))

    input_YoutubeIntend = Column(String, index=True, default='None')
    output_YoutubeIntend = Column(String, index=True, default='None')

    classification = relationship("classifications", back_populates="intends")


class wikipedia_intends(Base, BaseCRUD):
    __tablename__ = 'wikipedia_intends'
    id = Column(Integer, primary_key=True)
    classification_id = Column(Integer, ForeignKey('classification.id'))

    input_wikipedia = Column(String, index=True, default='None')
    output_wikipedia = Column(String, index=True, default='None')

    classification = relationship("classifications")


class studienordnung_intends(Base, BaseCRUD):
    __tablename__ = 'studienordnung_intends'
    id = Column(Integer, primary_key=True)
    classification_id = Column(Integer, ForeignKey('classification.id'))

    input_studienordnung = Column(String, index=True, default='None')
    output_studienordnung = Column(String, index=True, default='None')

    classification = relationship("classifications")


class todo_intends(Base, BaseCRUD):
    __tablename__ = 'todo_intends'
    id = Column(Integer, primary_key=True)
    classification_id = Column(Integer, ForeignKey('classification.id'))

    input_to_do_liste = Column(String, index=True, default='None')
    output_to_do_liste = Column(String, index=True, default='None')

    classification = relationship("classifications")


# Erstelle die Tabellen
Base.metadata.create_all(engine)
