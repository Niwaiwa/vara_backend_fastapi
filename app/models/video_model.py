import uuid
from sqlalchemy import String, Boolean, DateTime, Text, ForeignKey, Integer, CHAR
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from app.db.base import Base


class Video(Base):
    __tablename__ = "videos"

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[UUID] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    video_file: Mapped[str] = mapped_column(String(100), nullable=True)
    video_url: Mapped[str] = mapped_column(String(255), nullable=True)
    rating: Mapped[str] = mapped_column(CHAR(2), nullable=False, default="G")
    views_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    likes_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", foreign_keys=[user_id])
    video_likes = relationship("VideoLike", foreign_keys=[id], primaryjoin="Video.id==VideoLike.video_id")
    tags = relationship("Tag", secondary="video_tags", back_populates="videos")


    def increment_views_count(self):
        self.views_count += 1

    def increment_likes_count(self):
        self.likes_count += 1

    def decrement_likes_count(self):
        self.likes_count -= 1


class VideoLike(Base):
    __tablename__ = "video_likes"

    id = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = mapped_column(UUID(as_uuid=True), ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    video_id = mapped_column(UUID(as_uuid=True), ForeignKey('videos.id', ondelete='CASCADE'), nullable=False)
    created_at = mapped_column(DateTime, default=datetime.utcnow)
