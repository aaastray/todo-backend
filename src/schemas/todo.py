from pydantic import BaseModel
from typing import Optional
from uuid import UUID

class ToDoCreate(BaseModel):
    title: str
    completed: bool | None = False

class ToDoFromDB(ToDoCreate):
    id: UUID

class ToDoUpdate(BaseModel):
    title: Optional[str] = None
    completed: Optional[bool] = None