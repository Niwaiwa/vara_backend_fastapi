import logging
import uuid
from typing import Any, Annotated

from fastapi import APIRouter, Body, Depends, HTTPException
from sqlalchemy.orm import Session

from app import schemas, models
from app.usecase.user_usecase import UserUseCase
from app.repositories.user_repository import UserRepository
from app.db.database import get_db_connection
from app.core.deps import get_current_user

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/{user_id}", response_model=schemas.User)
def read_user_by_id(
    user_id: uuid.UUID,
    current_user: models.User = Depends(get_current_user)
) -> Any:
    """
    Get a specific user by id.
    """
    return current_user


@router.put("/{user_id}", response_model=schemas.User)
def update_user(
    user_id: uuid.UUID,
    user: schemas.UserUpdate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db_connection),
) -> Any:
    """
    Update a user.
    """
    user_usecase = UserUseCase(UserRepository(db))
    return user_usecase.update(current_user.id, user)

