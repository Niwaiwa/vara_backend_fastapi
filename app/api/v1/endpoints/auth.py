import logging
from datetime import timedelta
from typing import Any, Annotated
from pydantic import EmailStr

from fastapi import Depends, HTTPException, APIRouter, Form
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app import models, schemas
from app.core.security import create_access_token
from app.core.deps import get_current_user
from app.core.security import get_password_hash
from app.config import get_settings
from app.usecase.user_usecase import UserUseCase
from app.repositories.user_repository import UserRepository
from app.db.database import get_db_connection


logger = logging.getLogger(__name__)
env = get_settings()
router = APIRouter()


@router.post("/login", response_model=schemas.LoginUserResponse)
def login_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db_connection),
) -> Any:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    logger.info(f"form_data: {form_data.__dict__}")
    user_usecase = UserUseCase(UserRepository(db))
    user = user_usecase.authenticate(
        form_data.username, form_data.password
    )
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    # elif not user_usecase.is_active(user):
    #     raise HTTPException(status_code=400, detail="Inactive user")
    access_token_expires = timedelta(minutes=env.ACCESS_TOKEN_EXPIRE_MINUTES)
    return {
        "access_token": create_access_token(
            user.id, expires_delta=access_token_expires
        ),
        "token_type": "bearer",
    }

@router.post("/register", response_model=schemas.RegisterUserResponse)
def register_user(
    username: Annotated[str, Form()],
    email: Annotated[EmailStr, Form()],
    password: Annotated[str, Form()],
    db: Session = Depends(get_db_connection),
) -> Any:
    """
    Register new user.
    """
    form_data = schemas.RegisterUser(username=username, email=email, password=password)
    logger.info(f"username: {username}, email: {email}")

    user_usecase = UserUseCase(UserRepository(db))
    user = user_usecase.get_by_username(form_data.username)
    if user:
        raise HTTPException(status_code=400, detail="Username already registered")
    user = user_usecase.get_by_email(form_data.email)
    if user:
        raise HTTPException(status_code=400, detail="Email already registered")
    user = user_usecase.create(
        schemas.UserCreate(
            username=form_data.username,
            email=form_data.email,
            password=form_data.password,
        )
    )
    access_token_expires = timedelta(minutes=env.ACCESS_TOKEN_EXPIRE_MINUTES)
    return {
        "access_token": create_access_token(
            user.id, expires_delta=access_token_expires
        ),
        "token_type": "bearer",
    }


@router.post("/test-token", response_model=schemas.User)
def test_token(current_user: models.User = Depends(get_current_user)) -> Any:
    """
    Test access token
    """
    return current_user