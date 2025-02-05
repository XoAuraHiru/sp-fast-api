from datetime import datetime
from typing import Optional

from pydantic import Field, BaseModel


class UserBase(BaseModel):
    email: str = Field(..., min_length=3)
    password: str = Field(..., min_length=8)
    name: str = Field(..., min_length=3)
    is_active: bool = True

    class Config:
        json_schema_extra = {
            "example": {
                "email": "<EMAIL>",
                "password": "<PASSWORD>",
                "name": "John Doe",
                "is_active": True
            }
        }


class UserCreate(UserBase):
    pass

class UserUpdate(UserBase):
    pass

class UserResponse(UserBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True

class User(UserBase):
    id: int
    class Config:
        from_attributes = True