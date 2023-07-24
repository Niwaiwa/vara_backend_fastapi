import logging
import uuid
from typing import Any, Annotated

from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session

from app import schemas, models
from app.usecase.friend_usecase import FriendUseCase
from app.usecase.friend_request_usecase import FriendRequestUseCase
from app.repositories.friend_repository import FriendRepository
from app.repositories.friend_request_repository import FriendRequestRepository
from app.db.database import get_db_connection
from app.core.deps import get_current_user

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/{user_id}/friends")
def get_friend(
    user_id: uuid.UUID,
    page: int = 1,
    limit: int = 30,
    db: Session = Depends(get_db_connection),
    current_user: models.User = Depends(get_current_user),
) -> Any:
    """
    Get user's friend list.
    """
    friend_usercase = FriendUseCase(FriendRepository(db))
    data = friend_usercase.get_friend_list_by_user_id_and_offset_and_limit(current_user.id, (page - 1) * limit, limit)
    count = friend_usercase.get_friend_count(current_user.id)
    response_data = [schemas.FriendUser(
        id=user.id,
        username=user.username,
        nickname=user.nickname,
        avatar=user.avatar,
    ) for user in data]
    return {
        'data': response_data,
        'page': page,
        'count': count,
    }


@router.post("/{user_id}/friends")
def create_friend(
    user_id: uuid.UUID,
    friend_data: schemas.FriendUserID,
    db: Session = Depends(get_db_connection),
    current_user: models.User = Depends(get_current_user),
) -> Any:
    """
    Create a friend.
    """
    friend_request_usercase = FriendRequestUseCase(FriendRequestRepository(db))
    friend_usercase = FriendUseCase(FriendRepository(db))
    if current_user.id == friend_data.friend_user_id:
        raise HTTPException(status_code=400, detail="Can't add yourself as a friend")
    
    if friend_usercase.is_friend(current_user.id, friend_data.friend_user_id):
        raise HTTPException(status_code=400, detail="Friend already exists")

    if friend_request_usercase.is_friend_request(current_user.id, friend_data.friend_user_id):
        raise HTTPException(status_code=400, detail="Friend request already exists")
    
    if friend_request_usercase.is_friend_request(friend_data.friend_user_id, current_user.id):
        friend_request_usercase.delete_by_from_user_id_and_to_user_id(friend_data.friend_user_id, current_user.id)
        friend_usercase.create(schemas.FriendCreate(
            user_id=current_user.id,
            friend_user_id=friend_data.friend_user_id,
        ))
        friend_usercase.create(schemas.FriendCreate(
            user_id=friend_data.friend_user_id,
            friend_user_id=current_user.id,
        ))
        return {
            'message': 'success',
        }

    friend_usercase.create(schemas.FriendCreate(
        user_id=current_user.id,
        friend_user_id=friend_data.friend_user_id,
    ))
    return {
        'message': 'success',
    }


@router.delete("/{user_id}/friends")
def delete_friend(
    user_id: uuid.UUID,
    friend_data: schemas.FriendUserID,
    db: Session = Depends(get_db_connection),
    current_user: models.User = Depends(get_current_user),
) -> Any:
    """
    Delete a friend.
    """
    friend_usercase = FriendUseCase(FriendRepository(db))
    if current_user.id == friend_data.friend_user_id:
        raise HTTPException(status_code=400, detail="Can't delete yourself as a friend")

    if not friend_usercase.is_friend(current_user.id, friend_data.friend_user_id):
        raise HTTPException(status_code=400, detail="Friend not exists")

    friend_usercase.delete_by_user_id_and_friend_user_id(current_user.id, friend_data.friend_user_id)
    friend_usercase.delete_by_user_id_and_friend_user_id(friend_data.friend_user_id, current_user.id)
    return None
