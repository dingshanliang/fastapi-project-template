from typing import List

from fastapi import APIRouter, Response, Depends, Request

import schemas.role
from core.auth import get_current_active_superuser
from db.crud import crud_role
from db.session import get_db

roles_router = r = APIRouter()


# 获取所有角色
@r.get(
    '/roles',
    response_model=List[schemas.role.Role],
    response_model_exclude_none=True,
)
def roles_list(request: Request,
               response: Response,
               db=Depends(get_db),
               current_user=Depends(get_current_active_superuser),
               ):
    roles = crud_role.role.get_multi(db)
    return roles


# 获取特定 role_id 角色
@r.get('/roles/{role_id}', response_model=schemas.role.Role, response_model_exclude_none=True)
def role_details(
        request: Request,
        role_id: int,
        db=Depends(get_db),
        current_user=Depends(get_current_active_superuser),
):
    role = crud_role.role.get(db, role_id)
    return role


# 创建新角色
@r.post('/roles', response_model=schemas.role.Role, response_model_exclude_none=True)
def role_create(
        request: Request,
        role: schemas.role.RoleCreate,
        db=Depends(get_db),
        current_user=Depends(get_current_active_superuser),
):
    return crud_role.role.create(db, role)


# 更新信息
@r.put("/roles/{role_id}", response_model=schemas.role.Role, response_model_exclude_none=True)
def role_edit(
        request: Request,
        role_id: int,
        role: schemas.role.RoleUpdate,
        db=Depends(get_db),
        current_user=Depends(get_current_active_superuser),
):
    return crud_role.role.update(db, role_id, role)


# 删除角色
@r.delete("/roles/{role_id}", response_model=schemas.role.Role, response_model_exclude_none=True)
def role_delete(
        request: Request,
        role_id: int,
        db=Depends(get_db),
        current_user=Depends(get_current_active_superuser),
):
    return crud_role.role.delete(db, role_id)
