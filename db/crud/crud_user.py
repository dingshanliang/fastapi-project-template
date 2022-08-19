from typing import Optional

from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from starlette import status

from core.security import get_password_hash
from db.crud.base import CRUDBase
from models.user import User
from schemas.user import UserCreate, UserUpdate


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    def get_by_email(self, db: Session, email: str) -> Optional[User]:
        user = db.query(User).filter(User.email == email).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=self.model.__class__.__name__ + "not found"
            )
        return user

    def create(self, db: Session, user_in: UserCreate) -> User:
        hashed_password = get_password_hash(user_in.password) # 密码 hash 化
        user_in_data = jsonable_encoder(user_in)    # 将user_in 变为字典
        del user_in_data['password'] # 删除原始密码键值对
        user_in_data.update({'hashed_password': hashed_password}) # 增加hash 化后的密码键值对
        db_user = self.model(**user_in_data) # 生成 ORM 对象
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    def update(self, db: Session, user_id: int, user: UserUpdate) -> User:
        db_user = self.get(db, user_id)
        if not db_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=self.model.__class__.__name__ + "not found"
            )
        if user.password:
            user.password = get_password_hash(user.password)

        user_data = jsonable_encoder(user)
        db_user = self.model(**user_data)
        return db_user

user = CRUDUser(User)

