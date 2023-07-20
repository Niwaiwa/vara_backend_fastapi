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


class ProfileResponse(BaseModel):
    id: Optional[uuid.UUID] = None
    username: Optional[str] = None
    nickname: Optional[str] = None
    avatar: Optional[str] = None
    header: Optional[str] = None
    description: Optional[str] = None
    