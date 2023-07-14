from app.core.security import get_password_hash
from app.repositories.user_repository import UserRepository


class UserUseCase:
    def __init__(self, userRepository: UserRepository) -> None:
        self.userRepository = userRepository

    def create(self, user):
        hashed_password = get_password_hash(user.password)
        return self.userRepository.create(user, hashed_password)
    
    def get_by_username(self, username):
        return self.userRepository.get_by_username(username)
    
    def get_by_email(self, email):
        return self.userRepository.get_by_email(email)
    
    def get(self, id):
        return self.userRepository.get(id)
    
    def get_multi(self, skip: int = 0, limit: int = 100):
        return self.userRepository.get_multi(skip, limit)
    
    def update(self, id, user):
        db_user = self.userRepository.get(id)
        return self.userRepository.update(db_user, user)
    
    def update_password(self, id, password):
        db_user = self.userRepository.get(id)
        hashed_password = get_password_hash(password)
        return self.userRepository.update(db_user, {'password': hashed_password})
    
    def delete(self, id):
        return self.userRepository.delete(id)
    
    def authenticate(self, username: str, password: str):
        user = self.userRepository.get_by_username(username)
        if not user:
            return None
        if not get_password_hash(password) == user.password:
            return None
        return user
    
    def is_active(self, user):
        return user.is_active
    
    def is_superuser(self, user):
        return user.is_superuser