from pydantic import BaseModel

class RoleBase(BaseModel):
    role_name: str = 'user'

class Role(RoleBase):
    id: int
    class Config:
        orm_mode = True

class RoleCreate(RoleBase):
    class Config:
        orm_mode = True

class RoleEdit(RoleBase):
    class Config:
        orm_mode = True
