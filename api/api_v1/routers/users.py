from typing import List
from fastapi import APIRouter, Response, Depends, Request

from core.auth import get_current_active_superuser, get_current_active_user
from db.session import get_db
from schemas.user import User, UserCreate, UserUpdate
from db.crud import crud_user
users_router = r = APIRouter()


# 获取用户
@r.get(
    '/users',
    response_model=List[User],
    response_model_exclude_none=True,
)
def users_list(
        response: Response,
        db=Depends(get_db),
        current_user=Depends(get_current_active_superuser),
):
    users = crud_user.user.get_multi(db)

    response.headers["Content-Range"] = f"0-9/{len(users)}"
    return users


# 获取当前用户
@r.get('/users/me', response_model=User, response_model_exclude_none=True)
def user_me(current_user=Depends(get_current_active_user)):
    return current_user


# 获取特定 user_id 用户
@r.get('/users/{user_id}', response_model=User, response_model_exclude_none=True)
def user_details(
        request: Request,
        user_id: int,
        db=Depends(get_db),
        current_user=Depends(get_current_active_superuser),
):
    user = crud_user.user.get(db, user_id)
    return user


# 创建新用户
@r.post('/users', response_model=User, response_model_exclude_none=True)
def user_create(
        user: UserCreate,
        db=Depends(get_db),
        current_user=Depends(get_current_active_superuser),
):
    return crud_user.user.create(db, user)


# 更新用户信息
@r.put("/users/{user_id}", response_model=User, response_model_exclude_none=True)
def user_edit(
        request: Request,
        user_id: int,
        user: UserUpdate,
        db=Depends(get_db),
        current_user=Depends(get_current_active_superuser),
):
    return crud_user.user.update(db, user_id, user)


# 删除用户
@r.delete("/users/{user_id}", response_model=User, response_model_exclude_none=True)
def user_delete(
        request: Request,
        user_id: int,
        db=Depends(get_db),
        current_user=Depends(get_current_active_superuser),
):
    return crud_user.user.delete(db, user_id)
