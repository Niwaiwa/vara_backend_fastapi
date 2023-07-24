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


@router.get("/{user_id}/friends/requests")
def get_friend_request(
    user_id: uuid.UUID,
    page: int = 1,
    limit: int = 30,
    db: Session = Depends(get_db_connection),
    current_user: models.User = Depends(get_current_user),
) -> Any:
    """
    Get user's friend request list.
    """
    friend_request_usercase = FriendRequestUseCase(FriendRequestRepository(db))
    data = friend_request_usercase.get_friend_request_list_by_to_user_id_and_offset_and_limit(current_user.id, (page - 1) * limit, limit)
    count = friend_request_usercase.get_friend_request_count_by_to_user_id(current_user.id)
    response_data = [schemas.FriendRequestUser(
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


@router.post("/{user_id}/friends/requests/accept")
def accept_friend_request(
    user_id: uuid.UUID,
    friend_request_data: schemas.FriendRequestUserID,
    db: Session = Depends(get_db_connection),
    current_user: models.User = Depends(get_current_user),
) -> Any:
    """
    Accept a friend request.
    """
    friend_request_usercase = FriendRequestUseCase(FriendRequestRepository(db))
    friend_usercase = FriendUseCase(FriendRepository(db))
    if current_user.id == friend_request_data.user_id:
        raise HTTPException(status_code=400, detail="Invalid friend request.")
    if not friend_request_usercase.is_friend_request(friend_request_data.user_id, current_user.id):
        raise HTTPException(status_code=400, detail="You don't have a friend request from this user.")
    friend_request_usercase.delete_by_from_user_id_and_to_user_id(friend_request_data.user_id, current_user.id)
    friend_usercase.create(schemas.FriendCreate(
        user_id=friend_request_data.user_id,
        friend_user_id=current_user.id,
    ))
    friend_usercase.create(schemas.FriendCreate(
        user_id=current_user.id,
        friend_user_id=friend_request_data.user_id,
    ))
    return {
        'message': 'Success',
    }


@router.post("/{user_id}/friends/requests/reject")
def reject_friend_request(
    user_id: uuid.UUID,
    friend_request_data: schemas.FriendRequestUserID,
    db: Session = Depends(get_db_connection),
    current_user: models.User = Depends(get_current_user),
) -> Any:
    """
    Reject a friend request.
    """
    friend_request_usercase = FriendRequestUseCase(FriendRequestRepository(db))
    if current_user.id == friend_request_data.user_id:
        raise HTTPException(status_code=400, detail="Invalid friend request.")
    if not friend_request_usercase.is_friend_request(friend_request_data.user_id, current_user.id):
        raise HTTPException(status_code=400, detail="You don't have a friend request from this user.")
    friend_request_usercase.delete_by_from_user_id_and_to_user_id(friend_request_data.user_id, current_user.id)
    return {
        'message': 'Success',
    }


@router.post("/{user_id}/friends/requests/cancel")
def cancel_friend_request(
    user_id: uuid.UUID,
    friend_request_data: schemas.FriendUserID,
    db: Session = Depends(get_db_connection),
    current_user: models.User = Depends(get_current_user),
) -> Any:
    """
    Cancel a friend request.
    """
    friend_request_usercase = FriendRequestUseCase(FriendRequestRepository(db))
    if current_user.id == friend_request_data.friend_user_id:
        raise HTTPException(status_code=400, detail="Invalid friend request.")
    if not friend_request_usercase.is_friend_request(current_user.id, friend_request_data.friend_user_id):
        raise HTTPException(status_code=400, detail="You don't have a friend request to this user.")
    friend_request_usercase.delete_by_from_user_id_and_to_user_id(current_user.id, friend_request_data.friend_user_id)
    return {
        'message': 'Success',
    }