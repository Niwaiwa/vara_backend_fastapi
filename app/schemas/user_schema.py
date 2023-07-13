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


class UserUpdatePassword(UserBase):
    password: Optional[str] = None


class UserUpdate(UserBase):
    nickname: Optional[str] = None
    avatar: Optional[str] = None
    header: Optional[str] = None
    description: Optional[str] = None


class UserInDBBase(UserBase):
    id: Optional[int] = None

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