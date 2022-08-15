from pydantic import BaseModel
from typing import Optional


class UserBase(BaseModel):
    email: str
    is_active: bool = True
    is_superuser: bool = False
    first_name: str = None
    last_name: str = None

class User(UserBase):
    id: int

    class Config:
        orm_mode = True

class UserOut(UserBase):
    pass

class UserEdit(UserBase):
    password: Optional[str] = None

    class Config:
        orm_mode = True

class UserCreate(UserBase):
    password: str

    class Config:
        orm_mode = True