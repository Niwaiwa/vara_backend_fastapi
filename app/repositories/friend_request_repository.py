import uuid
from typing import Any, Dict, Optional

from sqlalchemy.orm import Session

from app.models.user_model import User
from app.models.friend_request_model import FriendRequest
from app.repositories.base_repository import BaseRepository
from app.schemas.friend_schema import FriendRequestCreate, FriendRequestUpdate


class FriendRequestRepository(BaseRepository[FriendRequest, FriendRequestCreate, FriendRequestUpdate]):

    def __init__(self, db: Session):
        super().__init__(FriendRequest, db)

    def get(self, id: Any) -> Optional[FriendRequest]:
        return self.db.query(FriendRequest).filter(FriendRequest.id == id).first()
    
    def get_multi(self, skip: int = 0, limit: int = 100) -> list:
        return self.db.query(FriendRequest).offset(skip).limit(limit).all()
    
    def get_friend_request(self, from_user_id: Any, to_user_id: Any) -> list:
        return self.db.query(FriendRequest).filter(FriendRequest.from_user_id == from_user_id).filter(FriendRequest.to_user_id == to_user_id).all()
    
    def create(self, obj_in: FriendRequestCreate) -> FriendRequest: 
        db_obj = FriendRequest(
            from_user_id=obj_in.from_user_id,
            to_user_id=obj_in.to_user_id,
        )
        self.db.add(db_obj)
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj
    
    def delete(self, id: uuid.UUID) -> FriendRequest:
        obj = self.db.query(FriendRequest).get(id)
        self.db.delete(obj)
        self.db.commit()
        return obj
    
    def delete_by_from_user_id_and_to_user_id(self, from_user_id: uuid.UUID, to_user_id: uuid.UUID) -> None:
        self.db.query(FriendRequest).filter(FriendRequest.from_user_id == from_user_id).filter(FriendRequest.to_user_id == to_user_id).delete()
        self.db.commit()
        return None
    
    def is_friend_request(self, from_user_id: uuid.UUID, to_user_id: uuid.UUID) -> bool:
        return self.db.query(FriendRequest).filter(FriendRequest.from_user_id == from_user_id).filter(FriendRequest.to_user_id == to_user_id).first() is not None
    
    def get_friend_request_count(self, from_user_id: uuid.UUID) -> int:
        return self.db.query(FriendRequest).filter(FriendRequest.from_user_id == from_user_id).count()
    
    def get_friend_request_list_by_from_user_id(self, from_user_id: uuid.UUID) -> list:
        return self.db.query(FriendRequest).filter(FriendRequest.from_user_id == from_user_id).all()
    
    def get_friend_request_list_by_from_user_id_and_offset_and_limit(self, from_user_id: uuid.UUID, offset: int = 0, limit: int = 100) -> list:
        friend_request_list = self.db.query(FriendRequest, User).join(User, User.id == FriendRequest.to_user_id). \
            filter(FriendRequest.from_user_id == from_user_id).offset(offset).limit(limit).all()
        return [friend_request.User for friend_request in friend_request_list]

    def get_friend_request_list_by_from_user_id_and_offset_and_limit_and_keyword(
            self, from_user_id: uuid.UUID, offset: int = 0, limit: int = 100, keyword: str = "") -> list:
        friend_request_list = self.db.query(FriendRequest, User).join(User, User.id == FriendRequest.to_user_id). \
            filter(FriendRequest.from_user_id == from_user_id).filter(User.name.like(f"%{keyword}%")).offset(offset).limit(limit).all()
        return [friend_request.User for friend_request in friend_request_list]
