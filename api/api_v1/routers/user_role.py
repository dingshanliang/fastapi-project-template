# 对用户的角色属性进行 CRUD 操作
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from starlette import status

import schemas.role
import schemas.user
from core.auth import get_current_active_superuser
from db.crud import crud_user
from db.crud import crud_role
from db.session import get_db

user_role_router = r = APIRouter()

# 为用户添加角色
@r.post(
    'user/role/{user_id}',
    response_model=schemas.user.UserOut
)
def add_user_role(
        user_id: int, # 给哪个用户
        roles: List[schemas.role.Role], # 添加什么角色
        db=Depends(get_db),
):
    # 根据 user_id 在数据库中获取用户
    db_user = crud_user.user.get(db, user_id)
    # 根据 roles 获取 db_roles
    db_roles = []
    for role in roles:
        db_roles.append(crud_role.role.get_role_by_code(db, role.role_code))
    # 求新增角色列表 和 原有角色列表的 并集
    merge_roles = list(set(db_roles) | set(db_user.roles))
    # 清空原有角色列表
    db_user.roles.clear()
    db_user.roles.extend(merge_roles)
    db.add(db_user)
    db.commit()
    return db_user

# 为用户删除角色
@r.delete('user/role/{user_id}', response_model=schemas.user.UserOut, response_model_exclude_none=True)
def delete_role(
        user_id: int, # 删除哪个用户
        roles: List[schemas.role.Role], # 添加什么角色
        db=Depends(get_db),
):
    # 根据 user_id 在数据库中获取用户
    db_user = crud_user.user.get(db, user_id)
    # 根据 roles 获取 db_roles
    db_roles = []
    for role in roles:
        db_roles.append(crud_role.role.get_role_by_code(db, role))
    # 原有角色列表 减去 待删除角色列表
    roles_left = list(set(db_user.roles) - set(db_roles))
    db_user.roles.clear()
    db_user.roles.extend(roles_left)

    return db_user

