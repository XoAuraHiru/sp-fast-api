from pydantic import Field


class UserBase:
    email: str = Field(..., min_length=3)
    password: str = Field(..., min_length=8)
    name: str = Field(..., min_length=3)
    is_active: bool = True


class UserCreate(UserBase):
    pass

class UserUpdate(UserBase):
    pass

class UserResponse(UserBase):
    id: int

    class Config:
        from_attributes = True

class User(UserBase):
    id: int
    class Config:
        from_attributes = True