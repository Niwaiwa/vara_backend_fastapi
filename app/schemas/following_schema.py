import uuid
from typing import Optional

from pydantic import BaseModel, EmailStr


class FollowingBase(BaseModel):
    user_id: uuid.UUID
    following_id: uuid.UUID


class FollowingCreate(FollowingBase):
    pass


class FollowingUpdate(FollowingBase):
    pass


class FollowingInDBBase(FollowingBase):
    id: Optional[uuid.UUID] = None

    class Config:
        orm_mode = True


class Following(FollowingInDBBase):
    pass