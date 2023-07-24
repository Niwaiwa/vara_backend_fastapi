import uuid
from typing import Optional

from pydantic import BaseModel

from app.schemas.user_schema import User


class FriendRequestBase(BaseModel):
    from_user_id: uuid.UUID
    to_user_id: uuid.UUID


class FriendRequestCreate(FriendRequestBase):
    pass


class FriendRequestUpdate(FriendRequestBase):
    pass


class FriendRequestUserID(BaseModel):
    user_id: uuid.UUID


class FriendRequestInDBBase(FriendRequestBase):
    id: Optional[uuid.UUID] = None

    class Config:
        orm_mode = True


class FriendRequest(FriendRequestInDBBase):
    pass


class FriendRequestResponse(BaseModel):
    id: Optional[uuid.UUID] = None
    from_user: Optional[User] = None
    to_user: Optional[User] = None


class FriendRequestListResponse(BaseModel):
    friend_request_list: list[FriendRequestResponse] = []
