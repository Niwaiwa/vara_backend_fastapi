import uuid
from typing import Any, Dict, Optional

from sqlalchemy.orm import Session

from app.models.user_model import User
from app.models.friend_model import Friend
from app.repositories.base_repository import BaseRepository
from app.schemas.friend_schema import FriendCreate, FriendUpdate


class FriendRepository(BaseRepository[Friend, FriendCreate, FriendUpdate]):

    def __init__(self, db: Session):
        super().__init__(Friend, db)

    def get(self, id: Any) -> Optional[Friend]:
        return self.db.query(Friend).filter(Friend.id == id).first()

    def get_multi(self, skip: int = 0, limit: int = 100) -> list:
        return self.db.query(Friend).offset(skip).limit(limit).all()

    def get_friend(self, user_id: Any) -> list:
        return self.db.query(Friend).filter(Friend.user_id == user_id).all()

    def create(self, obj_in: FriendCreate) -> Friend:
        db_obj = Friend(
            user_id=obj_in.user_id,
            friend_user_id=obj_in.friend_user_id,
        )
        self.db.add(db_obj)
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj

    def delete(self, id: uuid.UUID) -> Friend:
        obj = self.db.query(Friend).get(id)
        self.db.delete(obj)
        self.db.commit()
        return obj

    def delete_by_user_id_and_friend_user_id(self, user_id: uuid.UUID, friend_user_id: uuid.UUID) -> None:
        self.db.query(Friend).filter(Friend.user_id == user_id).filter(Friend.friend_user_id == friend_user_id).delete()
        self.db.commit()
        return None

    def is_friend(self, user_id: uuid.UUID, friend_user_id: uuid.UUID) -> bool:
        return self.db.query(Friend).filter(Friend.user_id == user_id).filter(Friend.friend_user_id == friend_user_id).first() is not None

    def get_friend_count(self, user_id: uuid.UUID) -> int:
        return self.db.query(Friend).filter(Friend.user_id == user_id).count()

    def get_friend_list_by_user_id(self, user_id: uuid.UUID) -> list:
        return self.db.query(Friend).filter(Friend.user_id == user_id).all()

    def get_friend_list_by_user_id_and_offset_and_limit(self, user_id: uuid.UUID, offset: int = 0, limit: int = 100) -> list:
        friend_list = self.db.query(Friend, User).join(User, User.id == Friend.friend_user_id). \
            filter(Friend.user_id == user_id).offset(offset).limit(limit).all()
        return [user for _, user in friend_list]

    def get_friend_list_by_user_id_and_offset_and_limit_and_keyword(self, user_id: uuid.UUID, offset: int = 0, limit: int = 100, keyword: str = "") -> list:
        friend_list = self.db.query(Friend, User).join(User, User.id == Friend.friend_user_id). \
            filter(Friend.user_id == user_id).filter(User.username == keyword).offset(offset).limit(limit).all()
        return [user for _, user in friend_list]
