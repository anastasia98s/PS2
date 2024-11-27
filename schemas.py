from pydantic import BaseModel
from typing import Optional

from enum import Enum

    
class ClassificationType(Enum):
    Youtube = "Youtube"
    Todo = "Todo"
    Wiki = "Wiki"
    studienordnung = "studienordnung"


    
# Pydantic-Modelle
class ClassificationSchema(BaseModel):
    id: Optional[int]
    Auswahl: ClassificationType

    class Config:
        from_attributes = True


class IntendSchema(BaseModel):
    id: Optional[int]
    classification_id: int
    input_YoutubeIntend: Optional[str]
    output_YoutubeIntend: Optional[str]

    class Config:
        from_attributes = True


class WikipediaIntendSchema(BaseModel):
    id: Optional[int]
    classification_id: int
    input_wikipedia: Optional[str]
    output_wikipedia: Optional[str]

    class Config:
        from_attributes = True


class StudienordnungIntendSchema(BaseModel):
    id: Optional[int]
    classification_id: int
    input_studienordnung: Optional[str]
    output_studienordnung: Optional[str]

    class Config:
        from_attributes = True


class TodoIntendSchema(BaseModel):
    id: Optional[int]
    classification_id: int
    input_to_do_liste: Optional[str]
    output_to_do_liste: Optional[str]

    class Config:
        from_attributes = True
