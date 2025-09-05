from sqlalchemy import create_engine, Column, Integer, String, Date, ForeignKey, BLOB
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    audio_features = Column(BLOB)
    # Relationship to access tasks associated with the user
    tasks = relationship("Task", back_populates="user")


class Task(Base):
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True, autoincrement=True)
    task = Column(String, nullable=False)
    due_date = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    user = relationship("User", back_populates="tasks")  # No trailing space here

# Create a new SQLite database (or connect to an existing one)
engine = create_engine('sqlite:///../../db.db')
Base.metadata.create_all(engine)

# Create a session
Session = sessionmaker(bind=engine)