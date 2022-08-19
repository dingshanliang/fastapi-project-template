from fastapi import HTTPException, Depends, status
import jwt
from jwt import PyJWTError

from core.security import SECRET_KEY, ALGORITHM, verify_password, oauth2_scheme
from db.session import get_db
from models.user import User
from schemas.token import TokenData
from schemas.user import UserCreate
from db.crud import crud_user


def get_current_user(
        db=Depends(get_db),
        token: str = Depends(oauth2_scheme)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="could not validate user credentials",
        headers={'WWW-Authenticate': 'bearer'}
    )
    try:
        # 从token 中解析出用户信息
        payload = jwt.decode(token, SECRET_KEY, algorithm=ALGORITHM)
        email: str = payload.get('sub')
        if email is None:
            raise credentials_exception
        permissions: str = payload.get('permissions')
        token_data = TokenData(email=email, permissions=permissions)
    except PyJWTError:
        raise credentials_exception
    user = crud_user.user.get_by_email(db, token_data.email)
    if user is None:
        raise credentials_exception
    return user


def get_current_active_user(
        current_user: User = Depends(get_current_user),
):
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="inactive user")
    return current_user


def get_current_active_superuser(
        current_user: User = Depends(get_current_active_user),
):
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=403,
            detail="用户权限不足"
        )
    return current_user


def authenticate_user(db, email: str, password: str):
    user = crud_user.user.get_by_email(db, email)
    if not user:
        return False  # user not exist
    if not verify_password(password, user.hashed_password):
        return False  # wrong password
    return user


def sign_up_new_user(db, email: str, password: str):
    try:
        user = crud_user.user.get_by_email(db, email)
        if user:
            return False  # user already exists
    except HTTPException:
        new_user = crud_user.user.create(
            db,
            UserCreate(
                email=email,
                password=password,
                is_active=True,
                is_superuer=False,
            ),
        )
        return new_user