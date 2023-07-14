import logging
import uuid
from typing import Any

from fastapi import APIRouter, Body, Depends, HTTPException
from sqlalchemy.orm import Session

from app import schemas
from app.usecase.user_usecase import UserUseCase
from app.repositories.user_repository import UserRepository
from app.db.database import get_db_connection

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/{user_id}", response_model=schemas.User)
def read_user_by_id(
    user_id: uuid.UUID,
    db: Session = Depends(get_db_connection),
) -> Any:
    """
    Get a specific user by id.
    """
    user_usecase = UserUseCase(UserRepository(db))
    user = user_usecase.get(user_id)
    logger.info(f"User: {user.__dict__}")
    # if not user or user.is_staff or user.is_superuser:
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
