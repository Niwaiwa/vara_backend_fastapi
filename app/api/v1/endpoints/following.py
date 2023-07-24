import logging
import uuid
import shutil
from typing import Any, Annotated

from fastapi import APIRouter, Body, Depends, File, Form, UploadFile
from fastapi.exceptions import HTTPException
from pydantic import EmailStr
from sqlalchemy.orm import Session

from app import schemas, models, config
from app.usecase.following_usecase import FollowingUseCase
from app.repositories.following_repository import FollowingRepository
from app.config import get_settings
from app.db.database import get_db_connection
from app.core.deps import get_current_user, upload_image

logger = logging.getLogger(__name__)
router = APIRouter()

@router.get("/{user_id}/following")
def get_following(
    user_id: uuid.UUID,
    page: int = 1,
    limit: int = 30,
    db: Session = Depends(get_db_connection),
) -> Any:
    """
    Get user's following list.
    """
    following_usercase = FollowingUseCase(FollowingRepository(db))
    data = following_usercase.get_following_list_by_user_id_and_offset_and_limit(user_id, (page - 1) * limit, limit)
    count = following_usercase.get_following_count(user_id)
    response_data = [schemas.FollowUser(
        username=user.username,
        nickname=user.nickname,
        avatar=user.avatar,
    ) for user in data]
    return {
        'data': response_data,
        'page': page,
        'count': count,
    }
    

@router.get("/{user_id}/follower")
def get_follower(
    user_id: uuid.UUID,
    page: int = 1,
    limit: int = 30,
    db: Session = Depends(get_db_connection),
) -> Any:
    """
    Get user's follower list.
    """
    following_usercase = FollowingUseCase(FollowingRepository(db))
    data = following_usercase.get_follower_list_by_user_id_and_offset_and_limit(user_id, (page - 1) * limit, limit)
    count = following_usercase.get_follower_count(user_id)
    response_data = [schemas.FollowUser(
        username=user.username,
        nickname=user.nickname,
        avatar=user.avatar,
    ) for user in data]
    return {
        'data': response_data,
        'page': page,
        'count': count,
    }


@router.post("/following") 
def create_following(
    following_user_id: schemas.FollowingUserID,
    db: Session = Depends(get_db_connection),
    current_user: models.User = Depends(get_current_user),
) -> Any:
    """
    Create following.
    """
    following_usercase = FollowingUseCase(FollowingRepository(db))
    if current_user.id == following_user_id.following_user_id:
        raise HTTPException(status_code=400, detail="Cannot follow yourself")

    if following_usercase.is_following(current_user.id, following_user_id.following_user_id):
        raise HTTPException(status_code=400, detail="Already following")

    create_following_data = schemas.FollowingCreate(
        user_id=current_user.id,
        following_user_id=following_user_id.following_user_id,
    )
    following_usercase.create(create_following_data)
    return None


@router.delete("/following")
def delete_following(
    following_user_id: schemas.FollowingUserID,
    db: Session = Depends(get_db_connection),
    current_user: models.User = Depends(get_current_user),
) -> Any:
    """
    Delete following.
    """
    following_usercase = FollowingUseCase(FollowingRepository(db))
    if current_user.id == following_user_id.following_user_id:
        raise HTTPException(status_code=400, detail="Cannot unfollow yourself")

    if not following_usercase.is_following(current_user.id, following_user_id.following_user_id):
        raise HTTPException(status_code=400, detail="Not following")

    following_usercase.delete_by_user_id_and_following_user_id(current_user.id, following_user_id.following_user_id)
    return None