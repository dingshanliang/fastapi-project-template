# from db.crud.base import CRUDBase
from typing import Optional

from fastapi import HTTPException
from sqlalchemy.orm import Session
from starlette import status

from schemas.role import RoleCreate, RoleUpdate
from .base import CRUDBase
from models.role import Role


class CRUDRole(CRUDBase[Role, RoleCreate, RoleUpdate]):
    def get_role_by_code(self, db: Session, code: str) -> Optional[Role]:
        result = db.query(self.model).filter(self.model.role_code == code).first()
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=self.model.__class__.__name__ + "not found",
            )
        return result



role = CRUDRole(Role)
