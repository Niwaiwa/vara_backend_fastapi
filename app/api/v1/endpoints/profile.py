import logging
import uuid
from typing import Any, Annotated

from fastapi import Depends, HTTPException, APIRouter, Form
from sqlalchemy.orm import Session

from app import models, schemas
from app.core.security import create_access_token
from app.core.deps import get_current_user, get_current_user_optional
from app.config import get_settings
from app.usecase.following_usecase import FollowingUseCase
from app.usecase.friend_usecase import FriendUseCase
from app.usecase.friend_request_usecase import FriendRequestUseCase
from app.usecase.user_usecase import UserUseCase
from app.repositories.following_repository import FollowingRepository
from app.repositories.friend_repository import FriendRepository
from app.repositories.friend_request_repository import FriendRequestRepository
from app.repositories.user_repository import UserRepository
from app.db.database import get_db_connection


logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/{username}", response_model=schemas.ProfileResponse)
def read_user_by_username(
    username: str,
    db: Session = Depends(get_db_connection),
    current_user: models.User = Depends(get_current_user_optional),
) -> Any:
    """
    Get a specific user by username.
    """
    user_usecase = UserUseCase(UserRepository(db))
    user = user_usecase.get_by_username(username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    is_following = False
    is_follower = False
    is_friend = False
    is_friend_request = False
    if current_user and current_user.username != username:
        following_usercase = FollowingUseCase(FollowingRepository(db))
        is_following = following_usercase.is_following(current_user.id, user.id)
        is_follower = following_usercase.is_follower(current_user.id, user.id)

        friend_usercase = FriendUseCase(FriendRepository(db))
        is_friend = friend_usercase.is_friend(current_user.id, user.id)
        friend_request_usercase = FriendRequestUseCase(FriendRequestRepository(db))
        is_friend_request = friend_request_usercase.is_friend_request(current_user.id, user.id)

    profile = schemas.ProfileResponse(
        id=user.id,
        username=user.username,
        nickname=user.nickname,
        avatar=user.avatar,
        header=user.header,
        description=user.description,
        is_following=is_following,
        is_follower=is_follower,
        is_friend=is_friend,
        is_friend_request=is_friend_request,
    )
    logger.info(f"profile: {profile}")
    return profile