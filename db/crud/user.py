from typing import List

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from core.security import get_password_hash
from schemas.user import UserBase, UserOut, UserCreate, UserEdit
# from models.user import User
import models.user


def get_user(db: Session, user_id: int):
    user = db.query(models.user.User).filter(models.user.User.id == user_id).first()
    # users = db.execute(select(User).filter_by(id = user_id))
    # user = users.scalars().first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


def get_user_by_email(db: Session, email: str) -> UserBase:
    # users = db.execute(select(User).filter_by(email = email))
    # user = users.scalars().first()
    # return user
    return db.query(models.user.User).filter(models.user.User.email == email).first()


def get_users(
        db: Session,
        skip: int = 0,
        limit: int = 100
) -> List[UserOut]:
    # users = db.execute(select(User).offset(skip).limit(limit))
    # users = users.scalars().all()
    users = db.query(models.user.User).offset(skip).limit(limit).all()
    return users


def create_user(db: Session, user: UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = models.user.User(
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        is_active=user.is_active,
        is_superuser=user.is_superuser,
        hashed_password=hashed_password,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id: int):
    user = get_user(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="user not found"
        )
    db.delete(user)
    db.commit()
    return user

def edit_user(db: Session, user_id: int, user: UserEdit) -> models.user.User:
    db_user = get_user(db, user_id)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="user not found"
        )
    update_data = user.dict(exclude_unset=True)

    if "password" in update_data:
        update_data["hashed_password"] = get_password_hash(user.password)
        del update_data["password"]

    for key, value in update_data.items():
        setattr(db_user, key, value)

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user