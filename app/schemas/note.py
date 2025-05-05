from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class Note(BaseModel):
    id: str
    title: str
    content: str
    created_at: datetime
    updated_at: datetime

class CreateNote(BaseModel):
    title: str
    content:str

class UpdateNote(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
