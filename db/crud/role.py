
from fastapi import HTTPException
from sqlalchemy.orm import Session
from starlette import status

import models.role
import schemas.role

# 根据id获取角色


def get_role(db: Session, role_id: int):
    role = db.query(models.role.Role).filter(models.role.Role.id == role_id).first()
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    return role

# 获取所有角色
def get_roles(db: Session):
    roles = db.query(models.role.Role).all()
    return roles

# 新建一个角色
def create_role(db: Session, role: schemas.role.RoleCreate):
    db_role = models.role.Role(role_name=role.role_name)
    db.add(db_role)
    db.commit()
    db.refresh(db_role)
    return db_role


# 删除一个角色
def delete_role(db: Session, role_id: int):
    role = get_role(db, role_id)
    if not role:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="role does not exist")
    db.delete(role)
    db.commit()
    return role

# 更新角色
def edit_role(db: Session, role_id: int, role: schemas.role.RoleEdit):
    db_role = get_role(db, role_id)
    if not db_role:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="role does not exist")
    update_data = role.dict(exclude_unset=True)

    for key, value in update_data.items():
        setattr(db_role, key, value)

    db.add(db_role)
    db.commit()
    db.refresh(db_role)
    return db_role
