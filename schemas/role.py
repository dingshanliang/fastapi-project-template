from pydantic import BaseModel

class RoleBase(BaseModel):
    role_code: str = None

class Role(RoleBase):
    class Config:
        orm_mode = True

class RoleCreate(RoleBase):
    role_name: str = 'user'
    class Config:
        orm_mode = True

class RoleUpdate(RoleBase):
    role_name: str = 'user'
    class Config:
        orm_mode = True

