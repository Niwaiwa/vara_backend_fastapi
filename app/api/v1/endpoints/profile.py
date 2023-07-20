import logging
import uuid
from typing import Any, Annotated

from fastapi import Depends, HTTPException, APIRouter, Form
from sqlalchemy.orm import Session

from app import models, schemas
from app.core.security import create_access_token
from app.core.deps import get_current_user
from app.config import get_settings
from app.usecase.user_usecase import UserUseCase
from app.repositories.user_repository import UserRepository
from app.db.database import get_db_connection


logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/{username}", response_model=schemas.ProfileResponse)
def read_user_by_username(
    username: str,
    db: Session = Depends(get_db_connection),
) -> Any:
    """
    Get a specific user by username.
    """
    user_usecase = UserUseCase(UserRepository(db))
    user = user_usecase.get_by_username(username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    profile = schemas.ProfileResponse(
        id=user.id,
        username=user.username,
        nickname=user.nickname,
        avatar=user.avatar,
        header=user.header,
        description=user.description,
    )
    logger.info(f"profile: {profile}")
    return profile