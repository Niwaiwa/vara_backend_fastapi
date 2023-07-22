import logging
import uuid
import shutil
from typing import Any, Annotated

from fastapi import APIRouter, Body, Depends, File, Form, UploadFile
from fastapi.exceptions import HTTPException
from pydantic import EmailStr
from sqlalchemy.orm import Session

from app import schemas, models, config
from app.usecase.user_usecase import UserUseCase
from app.repositories.user_repository import UserRepository
from app.config import get_settings
from app.db.database import get_db_connection
from app.core.deps import get_current_user, upload_image

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/", response_model=schemas.User)
def read_user_by_id(
    current_user: models.User = Depends(get_current_user)
) -> Any:
    """
    Get a specific user by id.
    """
    return current_user


@router.put("/", response_model=schemas.User)
def update_user(
    email: Annotated[EmailStr | None, Form()] = None,
    password: Annotated[str | None, Form()] = None,
    nickname: Annotated[str | None, Form()] = None,
    avatar: Annotated[UploadFile | None, File()] = None,
    header: Annotated[UploadFile | None, File()] = None,
    description: Annotated[str | None, Form()] = None,
    locale: Annotated[str | None, Form()] = None,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db_connection),
    settings: config.Settings = Depends(get_settings),
) -> Any:
    """
    Update a user.
    """
    avatar_filename = None
    header_filename = None

    if avatar:
        avatar_filename = upload_image(avatar, settings)

    if header:
        header_filename = upload_image(header, settings)

    user = schemas.UserUpdate(
        email=email,
        password=password,
        nickname=nickname,
        avatar=avatar_filename,
        header=header_filename,
        description=description,
        locale=locale,
    )
    user = user.dict(exclude_unset=True, exclude_none=True)
    user_usecase = UserUseCase(UserRepository(db))
    return user_usecase.update(current_user.id, user)
