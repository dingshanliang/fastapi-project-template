from typing import List
from fastapi import APIRouter, Response, Depends, Request

import schemas.role
from core.auth import get_current_active_superuser, get_current_active_user
import db.crud.role
from db.crud.role import get_role,get_roles,create_role,edit_role,delete_role
from db.crud.user import get_users, get_user, create_user, edit_user, delete_user
from db.session import get_db
from schemas.user import User, UserCreate, UserEdit

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
    roles = get_roles(db)
    return roles


# 获取特定 role_id 角色
@r.get('/roles/{role_id}', response_model=schemas.role.Role, response_model_exclude_none=True)
def role_details(
        request: Request,
        role_id: int,
        db=Depends(get_db),
        current_user=Depends(get_current_active_superuser),
):
    role = get_role(db, role_id)
    return role


# 创建新角色
@r.post('/roles', response_model=schemas.role.Role, response_model_exclude_none=True)
def role_create(
        request: Request,
        role: schemas.role.RoleCreate,
        db=Depends(get_db),
        current_user=Depends(get_current_active_superuser),
):
    return create_role(db, role)


# 更新信息
@r.put("/roles/{role_id}", response_model=schemas.role.Role, response_model_exclude_none=True)
def role_edit(
        request: Request,
        role_id: int,
        role: schemas.role.RoleEdit,
        db=Depends(get_db),
        current_user=Depends(get_current_active_superuser),
):
    return edit_role(db, role_id, role)


# 删除角色
@r.delete("/roles/{role_id}", response_model=schemas.role.Role, response_model_exclude_none=True)
def role_delete(
        request: Request,
        role_id: int,
        db=Depends(get_db),
        current_user=Depends(get_current_active_superuser),
):
    return delete_role(db, role_id)