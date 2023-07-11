from typing import Any, Dict, Optional, Union

from sqlalchemy.orm import Session

from app.core.security import get_password_hash
from app.models.user_model import User
from app.repositories.base_repository import BaseRepository
from app.schemas.user import UserCreate, UserUpdate

class UserRepository(BaseRepository[User, UserCreate, UserUpdate]):
    def get_by_username(self, db: Session, username: str) -> Optional[User]:
        return db.query(User).filter(User.username == username).first()

    def get_by_email(self, db: Session, email: str) -> Optional[User]:
        return db.query(User).filter(User.email == email).first()

    def get(self, db: Session, id: Any) -> Optional[User]:
        return db.query(User).filter(User.id == id).first()
    
    def get_multi(self, db: Session, skip: int = 0, limit: int = 100) -> list:
        return db.query(User).offset(skip).limit(limit).all()


    def create(self, db: Session, obj_in: UserCreate, hashed_password: str) -> User:
        db_obj = User(
            username=obj_in.username,
            email=obj_in.email,
            password=hashed_password,
            is_superuser=obj_in.is_superuser,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self, db: Session, db_obj: User, obj_in: Union[UserUpdate, Dict[str, Any]]
    ) -> User:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        if update_data["password"]:
            hashed_password = get_password_hash(update_data["password"])
            del update_data["password"]
            update_data["hashed_password"] = hashed_password
        return super().update(db, db_obj=db_obj, obj_in=update_data)
    
    def delete(self, db: Session, id: int) -> User:
        obj = db.query(User).get(id)
        db.delete(obj)
        db.commit()
        return obj

    # def authenticate(self, db: Session, *, email: str, password: str) -> Optional[User]:
    #     user = self.get_by_email(db, email=email)
    #     if not user:
    #         return None
    #     if not verify_password(password, user.hashed_password):
    #         return None
    #     return user

    # def is_active(self, user: User) -> bool:
    #     return user.is_active

    # def is_superuser(self, user: User) -> bool:
    #     return user.is_superuser
    
user = UserRepository(User)
