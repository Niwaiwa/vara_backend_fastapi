import logging

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
from app.repositories.user_repository import UserRepository

logger = logging.getLogger(__name__)
env = get_settings()

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"api/users/login"
)

def get_current_user(
    db: Session = Depends(get_db_connection),
    token: str = Depends(reusable_oauth2),
) -> models.User:
    try:
        payload = jwt.decode(
            token, env.SECRET_KEY, algorithms=[security.ALGORITHM]
        )
        token_data = schemas.TokenPayload(**payload)
    except (JWTError, ValidationError) as e:
        errmsg = str(e).replace('\n', ' ')
        logger.error(f"{type(e).__name__}: {errmsg}")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    user_usecase = UserUseCase(UserRepository(db))
    user = user_usecase.get(token_data.sub)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


def get_current_active_user(
    db: Session = Depends(get_db_connection),
    current_user: models.User = Depends(get_current_user),
) -> models.User:
    user_usecase = UserUseCase(UserRepository(db))
    if not user_usecase.is_active(current_user):
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


def get_current_active_superuser(
    db: Session = Depends(get_db_connection),
    current_user: models.User = Depends(get_current_user),
) -> models.User:
    user_usecase = UserUseCase(UserRepository(db))
    if not user_usecase.is_superuser(current_user):
        raise HTTPException(
            status_code=400, detail="The user doesn't have enough privileges"
        )
    return current_user