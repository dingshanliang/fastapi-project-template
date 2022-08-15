from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from core.auth import authenticate_user, sign_up_new_user
from core.security import ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token
from db.session import get_db

auth_router = r = APIRouter()


@r.post("/token")
def login(
        db=Depends(get_db),
        form_data: OAuth2PasswordRequestForm = Depends()
):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    if user.is_superuser:
        permissions = 'admin'
    else:
        permissions = 'user'
    access_token = create_access_token(
        data={"sub": user.email, "permissions": permissions},
        expires_delta=access_token_expires,
    )
    return {"access_token": access_token, "token_type": "bearer"}


@r.post('/signup')
def signup(
        db=Depends(get_db),
        form_data: OAuth2PasswordRequestForm = Depends(),
):
    user = sign_up_new_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="account already exists",
            headers={'WWW-Authenticate': "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    if user.is_superuser:
        permissions = 'admin'
    else:
        permissions = 'user'
    access_token = create_access_token(data={"sub": user.email, "permissions": permissions},
                                expires_delta=access_token_expires, )
    return {"access_token": access_token, "token_type": "bearer"}
