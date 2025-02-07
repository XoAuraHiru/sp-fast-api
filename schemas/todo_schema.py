from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

class TodoBase(BaseModel):
    title: str
    description: str
    completed: bool = False

class TodoCreate(TodoBase):
    pass

class TodoUpdate(TodoBase):
    pass

class TodoResponse(TodoBase):
    id: int
    user_id: int
    created_at: datetime