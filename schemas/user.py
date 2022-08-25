from pydantic import BaseModel
from typing import Optional, List


class UserBase(BaseModel):
    email: str
    is_active: bool = True
    is_superuser: bool = False
    first_name: str = None
    last_name: str = None
    # role_id: int = None
    # roles: List[str] = []

class User(UserBase):
    id: int

    class Config:
        orm_mode = True

class UserOut(UserBase):

    class Config:
        orm_mode = True

class UserUpdate(UserBase):
    password: Optional[str] = None

    class Config:
        orm_mode = True

class UserCreate(UserBase):
    password: str

    class Config:
        orm_mode = True