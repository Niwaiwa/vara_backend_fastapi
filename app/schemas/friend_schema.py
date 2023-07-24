import uuid
from typing import Optional

from pydantic import BaseModel

from app.schemas.user_schema import User


class FriendBase(BaseModel):
    user_id: uuid.UUID
    friend_user_id: uuid.UUID


class FriendCreate(FriendBase):
    pass


class FriendUpdate(FriendBase):
    pass


class FriendUserID(BaseModel):
    friend_user_id: uuid.UUID


class FriendInDBBase(FriendBase):
    id: Optional[uuid.UUID] = None

    class Config:
        orm_mode = True


class Friend(FriendInDBBase):
    pass


class FriendResponse(BaseModel):
    id: Optional[uuid.UUID] = None
    user: Optional[User] = None
    friend_user: Optional[User] = None


class FriendListResponse(BaseModel):
    friend_list: list[FriendResponse] = []

