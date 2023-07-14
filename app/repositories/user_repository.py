from typing import Any, Dict, Optional, Union

from sqlalchemy.orm import Session

from app.models.user_model import User
from app.repositories.base_repository import BaseRepository
from app.schemas.user_schema import UserCreate, UserUpdate


class UserRepository(BaseRepository[User, UserCreate, UserUpdate]):

    def __init__(self, db: Session):
        super().__init__(User, db)

    def get_by_username(self, username: str) -> Optional[User]:
        return self.db.query(User).filter(User.username == username).first()

    def get_by_email(self, email: str) -> Optional[User]:
        return self.db.query(User).filter(User.email == email).first()

    def get(self, id: Any) -> Optional[User]:
        return self.db.query(User).filter(User.id == id).first()
    
    def get_multi(self, skip: int = 0, limit: int = 100) -> list:
        return self.db.query(User).offset(skip).limit(limit).all()

    def create(self, obj_in: UserCreate, hashed_password: str) -> User:
        db_obj = User(
            username=obj_in.username,
            email=obj_in.email,
            password=hashed_password,
            is_superuser=obj_in.is_superuser,
        )
        self.db.add(db_obj)
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj

    def update(
        self, db_obj: User, obj_in: Union[UserUpdate, Dict[str, Any]]
    ) -> User:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        return super().update(db_obj=db_obj, obj_in=update_data)
    
    def delete(self, id: int) -> User:
        obj = self.db.query(User).get(id)
        self.db.delete(obj)
        self.db.commit()
        return obj
