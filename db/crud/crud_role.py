# from db.crud.base import CRUDBase
from schemas.role import RoleCreate, RoleUpdate
from .base import CRUDBase
from models.role import Role


class CRUDRole(CRUDBase[Role, RoleCreate, RoleUpdate]):
    pass

role = CRUDRole(Role)
