from typing import Generator

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from pydantic import ValidationError
from sqlalchemy.orm import Session

from app import models, schemas
from app.core import security
from app.config import get_settings
from app.db.database import get_db_connection
from app.usecase.user_usecase import UserUseCase


env = get_settings()

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"v1/login/access-token"
)

def get_current_user(
    token: str = Depends(reusable_oauth2),
    user_usecase: UserUseCase = Depends(),
) -> models.User:
    try:
        payload = jwt.decode(
            token, env.SECRET_KEY, algorithms=[security.ALGORITHM]
        )
        token_data = schemas.TokenPayload(**payload)
    except (JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    user = user_usecase.get(token_data.sub)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


def get_current_active_user(
    user_usecase: UserUseCase = Depends(),
    current_user: models.User = Depends(get_current_user),
) -> models.User:
    if not user_usecase.is_active(current_user):
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


def get_current_active_superuser(
    user_usecase: UserUseCase = Depends(),
    current_user: models.User = Depends(get_current_user),
) -> models.User:
    if not user_usecase.is_superuser(current_user):
        raise HTTPException(
            status_code=400, detail="The user doesn't have enough privileges"
        )
    return current_user