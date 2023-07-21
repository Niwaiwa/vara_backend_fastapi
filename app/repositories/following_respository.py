import uuid
from typing import Any, Dict, Optional

from sqlalchemy.orm import Session

from app.models.user_model import Following
from app.repositories.base_repository import BaseRepository
from app.schemas.following_schema import FollowingCreate, FollowingUpdate


class FollowingRepository(BaseRepository[Following, FollowingCreate, FollowingUpdate]):
    
    def __init__(self, db: Session):
        super().__init__(Following, db)

    def get(self, id: Any) -> Optional[Following]:
        return self.db.query(Following).filter(Following.id == id).first()
    
    def get_multi(self, skip: int = 0, limit: int = 100) -> list:
        return self.db.query(Following).offset(skip).limit(limit).all()
    
    def get_following(self, user_id: Any) -> list:
        return self.db.query(Following).filter(Following.user_id == user_id).all()
    
    def create(self, obj_in: FollowingCreate) -> Following:
        db_obj = Following(
            user_id=obj_in.user_id,
            following_id=obj_in.following_id,
        )
        self.db.add(db_obj)
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj
    
    def delete(self, id: uuid.UUID) -> Following:
        obj = self.db.query(Following).get(id)
        self.db.delete(obj)
        self.db.commit()
        return obj
        
    def delete_by_user_id_and_following_user_id(self, user_id: uuid.UUID, following_user_id: uuid.UUID) -> None:
        self.db.query(Following).filter(Following.user_id == user_id).filter(Following.following_user_id == following_user_id).delete()
        self.db.commit()
        return None
        
    def is_following(self, user_id: uuid.UUID, following_user_id: uuid.UUID) -> bool:
        return self.db.query(Following).filter(Following.user_id == user_id).filter(Following.following_user_id == following_user_id).first() is not None
    
    def get_following_count(self, user_id: uuid.UUID) -> int:
        return self.db.query(Following).filter(Following.user_id == user_id).count()
    
    def get_follower_count(self, following_user_id: uuid.UUID) -> int:
        return self.db.query(Following).filter(Following.following_user_id == following_user_id).count()

    def get_following_list_by_user_id(self, user_id: uuid.UUID) -> list:
        return self.db.query(Following).filter(Following.user_id == user_id).all()
    
    def get_follower_list_by_user_id(self, user_id: uuid.UUID) -> list:
        return self.db.query(Following).filter(Following.following_user_id == user_id).all()

    def get_following_list_by_user_id_and_offset_and_limit(self, user_id: uuid.UUID, offset: int, limit: int) -> list:
        return self.db.query(Following).filter(Following.user_id == user_id).offset(offset).limit(limit).all()
    
    def get_follower_list_by_user_id_and_offset_and_limit(self, user_id: uuid.UUID, offset: int, limit: int) -> list:
        return self.db.query(Following).filter(Following.following_user_id == user_id).offset(offset).limit(limit).all()
