import uuid
from typing import Optional

from pydantic import BaseModel, EmailStr


# Shared properties
class UserBase(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = True
    is_staff: bool = False
    is_superuser: bool = False


# Properties to receive via API on creation
class UserCreate(UserBase):
    username: str
    email: EmailStr
    password: str


class UserUpdatePassword(BaseModel):
    password: Optional[str] = None


class UserUpdate(UserUpdatePassword):
    email: Optional[EmailStr] = None
    nickname: Optional[str] = None
    avatar: Optional[str] = None
    header: Optional[str] = None
    description: Optional[str] = None
    locale: Optional[str] = None


class UserInDBBase(UserBase):
    id: Optional[uuid.UUID] = None

    class Config:
        orm_mode = True


class User(UserInDBBase):
    nickname: Optional[str] = None
    avatar: Optional[str] = None
    header: Optional[str] = None
    description: Optional[str] = None
    locale: Optional[str] = None
    last_login: Optional[str] = None


class UserInDB(UserInDBBase):
    hashed_password: str


class RegisterUser(BaseModel):
    username: str
    email: EmailStr
    password: str


class RegisterUserResponse(BaseModel):
    access_token: str
    token_type: str


class LoginUser(BaseModel):
    username: str
    password: str


class LoginUserResponse(BaseModel):
    access_token: str
    token_type: str


class ContentUser(BaseModel):
    username: Optional[str] = None
    nickname: Optional[str] = None
    avatar: Optional[str] = None
    is_following: Optional[bool] = False


class ProfileResponse(BaseModel):
    id: Optional[uuid.UUID] = None
    username: Optional[str] = None
    nickname: Optional[str] = None
    avatar: Optional[str] = None
    header: Optional[str] = None
    description: Optional[str] = None
    is_following: Optional[bool] = False
    is_follower: Optional[bool] = False
    is_friend: Optional[bool] = False
    is_friend_request: Optional[bool] = False


class FollowUser(BaseModel):
    username: Optional[str]
    nickname: Optional[str] = None
    avatar: Optional[str] = None

    class Config:
        orm_mode = True


class FollowUserListResponse(BaseModel):
    follow_user_list: list[FollowUser] = []
    page: int
    count: int

    class Config:
        orm_mode = True


class FriendUser(FollowUser):
    id: Optional[uuid.UUID] = None


class FriendUserListResponse(BaseModel):
    friend_user_list: list[FriendUser] = []
    page: int
    count: int

    class Config:
        orm_mode = True


class FriendRequestUser(FollowUser):
    id: Optional[uuid.UUID] = None


class FriendRequestUserListResponse(BaseModel):
    friend_request_user_list: list[FriendRequestUser] = []
    page: int
    count: int

    class Config:
        orm_mode = True