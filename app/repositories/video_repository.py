import uuid
from typing import Any, Dict, Optional, Union

from sqlalchemy.orm import Session, Query

from app.models.user_model import User
from app.models.video_model import Video, VideoLike
from app.models.tag_model import Tag
from app.repositories.base_repository import BaseRepository
from app.schemas.video_schema import VideoCreate, VideoUpdate


class VideoRepository(BaseRepository[Video, VideoCreate, VideoUpdate]):

    def __init__(self, db: Session):
        super().__init__(Video, db)

    def get(self, id: Any) -> Optional[Video]:
        return self.db.query(Video).filter(Video.id == id).first()

    def get_multi(self, skip: int = 0, limit: int = 100) -> list:
        return self.db.query(Video).offset(skip).limit(limit).all()

    def get_video(self, user_id: Any) -> list:
        return self.db.query(Video).filter(Video.user_id == user_id).all()

    def create(self, obj_in: VideoCreate, tags: list) -> Video:
        tags = self.db.query(Tag).filter(Tag.name.in_(tags)).all()
        db_obj = Video(
            user_id=obj_in.user_id,
            title=obj_in.title,
            description=obj_in.description,
            video_file=obj_in.video_file,
            video_url=obj_in.video_url,
            rating=obj_in.rating,
            tags=tags,
        )
        self.db.add(db_obj)
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj

    def update(self, id: uuid.UUID, obj_in: Union[VideoUpdate, Dict[str, Any]], tags: list) -> Video:
        obj = self.db.query(Video).get(id)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        
        tags = self.db.query(Tag).filter(Tag.name.in_(tags)).all()
        update_data['tags'] = tags

        for field in update_data:
            if field in update_data:
                setattr(obj, field, update_data[field])
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def delete(self, id: uuid.UUID) -> Video:
        obj = self.db.query(Video).get(id)
        self.db.delete(obj)
        self.db.commit()
        return obj

    def get_video_count(self, user_id: uuid.UUID) -> int:
        return self.db.query(Video).filter(Video.user_id == user_id).count()

    def get_video_list_by_user_id(self, user_id: uuid.UUID) -> list:
        return self.db.query(Video).filter(Video.user_id == user_id).all()

    def get_video_list_by_user_id_and_offset_and_limit(self, user_id: uuid.UUID, offset: int = 0, limit: int = 100) -> list:
        return self.db.query(Video).filter(Video.user_id == user_id).offset(offset).limit(limit).all()
    
    def get_video_list_by_user_id_and_offset_and_limit_count(self, user_id: uuid.UUID) -> int:
        return self.db.query(Video).filter(Video.user_id == user_id).count()
    
    def get_video_list_by_user_id_and_offset_and_limit_and_rating(self, user_id: uuid.UUID, offset: int = 0, limit: int = 100, rating: str = 'G') -> list:
        return self.db.query(Video).filter(Video.user_id == user_id).filter(Video.rating == rating).offset(offset).limit(limit).all()
    
    def get_video_list_by_user_id_and_offset_and_limit_and_rating_count(self, user_id: uuid.UUID, rating: str = 'G') -> int:
        return self.db.query(Video).filter(Video.user_id == user_id).filter(Video.rating == rating).count()

    def get_video_list_by_offset_and_limit_and_rating(self, offset: int = 0, limit: int = 100, rating: str = 'G') -> list:
        return self.db.query(Video).filter(Video.rating == rating).offset(offset).limit(limit).all()
    
    def get_video_list_by_offset_and_limit_and_rating_count(self, rating: str = 'G') -> int:
        return self.db.query(Video).filter(Video.rating == rating).count()

    def get_video_list_by_offset_and_limit_and_rating_and_keyword(self, offset: int = 0, limit: int = 100, rating: str = 'G', keyword: str = "") -> list:
        return self.db.query(Video).filter(Video.rating == rating).filter(Video.title.like(f'%{keyword}%')).offset(offset).limit(limit).all()

    def get_video_list_by_offset_and_limit_and_rating_and_keyword_count(self, rating: str = 'G', keyword: str = "") -> int:  
        return self.db.query(Video).filter(Video.rating == rating).filter(Video.title.like(f'%{keyword}%')).count()

    def get_video_list_by_offset_and_limit_and_rating_and_tag(self, offset: int = 0, limit: int = 100, rating: str = 'G', tag: str = "") -> list:
        return self.db.query(Video).filter(Video.rating == rating).filter(Tag.name == tag).offset(offset).limit(limit).all()
    
    def get_video_list_by_offset_and_limit_and_rating_and_tag_count(self, rating: str = 'G', tag: str = "") -> int:
        return self.db.query(Video).filter(Video.rating == rating).filter(Tag.name == tag).count()
    
    def get_video_list_by_offset_and_limit_and_rating_and_tags(self, offset: int = 0, limit: int = 100, rating: str = 'G', tags: list = []) -> list:
        return self.db.query(Video).distinct(Video.id).join(Video.tags).filter(Video.rating == rating).filter(Tag.name.in_(tags)).offset(offset).limit(limit).all()
    
    def get_video_list_by_offset_and_limit_and_rating_and_tags_count(self, rating: str = 'G', tags: list = []) -> int:
        return self.db.query(Video).distinct(Video.id).join(Video.tags).filter(Video.rating == rating).filter(Tag.name.in_(tags)).count()
    
    def get_video_list_by_offset_and_limit_and_rating_and_tags_and_sort_latest(self, offset: int = 0, limit: int = 100, rating: str = 'G', tags: list = []) -> list:
        q = self._query_video_by_tags(tags)
        return q.filter(Video.rating == rating).order_by(Video.created_at.desc()).offset(offset).limit(limit).all()
    
    def get_video_list_by_offset_and_limit_and_rating_and_tags_and_sort_latest_count(self, rating: str = 'G', tags: list = []) -> int:
        q = self._query_video_by_tags(tags)
        return q.filter(Video.rating == rating).order_by(Video.created_at.desc()).count()
    
    def get_video_list_by_offset_and_limit_and_rating_and_tags_and_sort_oldest(self, offset: int = 0, limit: int = 100, rating: str = 'G', tags: list = []) -> list:
        q = self._query_video_by_tags(tags)
        return q.filter(Video.rating == rating).order_by(Video.created_at.asc()).offset(offset).limit(limit).all()
    
    def get_video_list_by_offset_and_limit_and_rating_and_tags_and_sort_oldest_count(self, rating: str = 'G', tags: list = []) -> int:
        q = self._query_video_by_tags(tags)
        return q.filter(Video.rating == rating).order_by(Video.created_at.asc()).count()
    
    def get_video_list_by_offset_and_limit_and_rating_and_tags_and_sort_views(self, offset: int = 0, limit: int = 100, rating: str = 'G', tags: list = []) -> list:
        q = self._query_video_by_tags(tags)
        return q.filter(Video.rating == rating).order_by(Video.views_count.desc()).offset(offset).limit(limit).all()
    
    def get_video_list_by_offset_and_limit_and_rating_and_tags_and_sort_views_count(self, rating: str = 'G', tags: list = []) -> int:
        q = self._query_video_by_tags(tags)
        return q.filter(Video.rating == rating).order_by(Video.views_count.desc()).count()
    
    def get_video_list_by_offset_and_limit_and_rating_and_tags_and_sort_likes(self, offset: int = 0, limit: int = 100, rating: str = 'G', tags: list = []) -> list:
        q = self._query_video_by_tags(tags)
        return q.filter(Video.rating == rating).order_by(Video.likes_count.desc()).offset(offset).limit(limit).all()
    
    def get_video_list_by_offset_and_limit_and_rating_and_tags_and_sort_likes_count(self, rating: str = 'G', tags: list = []) -> int:
        q = self._query_video_by_tags(tags)
        return q.filter(Video.rating == rating).order_by(Video.likes_count.desc()).count()
    
    def _query_video_by_tags(self, tags: list) -> Query:
        q = self.db.query(Video)
        if tags:
            q = q.join(Video.tags).filter(Tag.name.in_(tags))
        return q
    
    def like_video(self, user_id: uuid.UUID, video_id: uuid.UUID) -> Video:
        video = self.db.query(Video).filter(Video.id == video_id).first()
        video.likes_count += 1
        video_like = VideoLike(user_id=user_id, video_id=video_id)
        self.db.add(video_like)
        self.db.add(video)
        self.db.commit()
        self.db.refresh(video)
        return video
    
    def unlike_video(self, user_id: uuid.UUID, video_id: uuid.UUID) -> Video:
        video = self.db.query(Video).filter(Video.id == video_id).first()
        video.likes_count -= 1
        video_like = self.db.query(VideoLike).filter(VideoLike.user_id == user_id).filter(VideoLike.video_id == video_id).first()
        self.db.delete(video_like)
        self.db.add(video)
        self.db.commit()
        self.db.refresh(video)
        return video