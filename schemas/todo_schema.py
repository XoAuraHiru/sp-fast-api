from datetime import datetime
from typing import Optional
from pydantic import Field, BaseModel

class TodoBase(BaseModel):
    title: str = Field(min_length=3, max_length=100)
    description: Optional[str] = Field(min_length=3, max_length=1000)
    priority: int = Field(gt=0, lt=6)
    completed: bool = False

    class Config:
        json_schema_extra = {
            "example": {
                "title": "Buy groceries",
                "description": "Buy milk, eggs, and bread",
                "priority": 3,
                "completed": False
            }
        }

class TodoCreate(TodoBase):
    pass

class TodoUpdate(TodoBase):
    pass

class TodoResponse(TodoBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime]

    class ModelValidate:
        from_attributes = True

class Todo(TodoBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True