from fastapi import Depends
from app.core.security import get_password_hash
from app.repositories.user_repository import UserRepository


class UserUseCase:
    userRepository: UserRepository

    def __init__(self, userRepository: UserRepository = Depends()) -> None:
        self.userRepository = userRepository

    def create(self, db, user):
        hashed_password = get_password_hash(user.password)
        return self.userRepository.create(db, user, hashed_password)
    
    def get_by_username(self, db, username):
        return self.userRepository.get_by_username(db, username)
    
    def get_by_email(self, db, email):
        return self.userRepository.get_by_email(db, email)
    
    def get(self, db, id):
        return self.userRepository.get(db, id)
    
    def get_multi(self, db, skip: int = 0, limit: int = 100):
        return self.userRepository.get_multi(db, skip, limit)
    
    def update(self, db, id, user):
        db_user = self.userRepository.get(db, id)
        return self.userRepository.update(db, db_user, user)
    
    def delete(self, db, id):
        return self.userRepository.delete(db, id)