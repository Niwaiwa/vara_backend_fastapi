import uuid
from sqlalchemy import String, ForeignKey, Integer, CHAR, Table, Column
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from app.db.base import Base


video_tags = Table(
    "video_tags",
    Base.metadata,
    Column("id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
    Column("tag_id", UUID(as_uuid=True), ForeignKey('tags.id', ondelete='CASCADE'), nullable=False, index=True),
    Column("video_id", UUID(as_uuid=True), ForeignKey('videos.id', ondelete='CASCADE'), nullable=False, index=True),
)


class Tag(Base):
    __tablename__ = "tags"

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    slug: Mapped[str] = mapped_column(String(255), nullable=False)

    videos = relationship("Video", secondary="video_tags", back_populates="tags")


# class VideoTag(Base):
#     __tablename__ = "video_tags"

#     id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
#     video_id: Mapped[UUID] = mapped_column(ForeignKey('videos.id', ondelete='CASCADE'), nullable=False, index=True)
#     tag_id: Mapped[UUID] = mapped_column(ForeignKey('tags.id', ondelete='CASCADE'), nullable=False, index=True)

    # video = relationship("Video", back_populates="tags")
    # tag = relationship("Tag", back_populates="videos")
