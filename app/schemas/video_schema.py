import uuid, datetime
from typing import Optional

from pydantic import BaseModel

from app.schemas.user_schema import User, ContentUser


class VideoBase(BaseModel):
    user_id: Optional[uuid.UUID] = None
    title: str
    description: str
    video_file: str | None = None
    video_url: str | None = None
    rating: str


class VideoCreate(VideoBase):
    pass


class VideoUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    rating: str | None = None
    tags: list[str] | None = None


class VideoInDBBase(VideoBase):
    id: Optional[uuid.UUID] = None
    views_count: Optional[int] = None
    likes_count: Optional[int] = None
    created_at: Optional[datetime.datetime] = None
    updated_at: Optional[datetime.datetime] = None

    class Config:
        orm_mode = True


class Video(VideoInDBBase):
    pass


class VideoResponse(BaseModel):
    id: Optional[uuid.UUID] = None
    user: Optional[ContentUser] = None
    title: Optional[str] = None
    description: Optional[str] = None
    video_file: Optional[str] = None
    video_url: Optional[str] = None
    rating: Optional[str] = None
    views_count: Optional[int] = None
    likes_count: Optional[int] = None
    created_at: Optional[datetime.datetime] = None
    updated_at: Optional[datetime.datetime] = None
    tags: Optional[list] = None
    is_liked: Optional[bool] = False


class VideoListResponse(BaseModel):
    video_list: list[VideoResponse] = []
    page: int
    count: int


class VideoLikeBase(BaseModel):
    user_id: uuid.UUID
    video_id: uuid.UUID


class VideoLikeCreate(VideoLikeBase):
    video_id: uuid.UUID


class VideoLikeUpdate(VideoLikeBase):
    pass


class VideoLikeInDBBase(VideoLikeBase):
    id: Optional[uuid.UUID] = None
    created_at: Optional[datetime.datetime] = None

    class Config:
        orm_mode = True


class VideoLike(VideoLikeInDBBase):
    pass
