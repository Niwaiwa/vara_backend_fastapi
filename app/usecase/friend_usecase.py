from app.repositories.friend_repository import FriendRepository


class FriendUseCase:

    def __init__(self, friend_repository: FriendRepository) -> None:
        self.friend_repository = friend_repository

    def get(self, id):
        return self.friend_repository.get(id)
    
    def get_multi(self, skip: int = 0, limit: int = 100):
        return self.friend_repository.get_multi(skip, limit)
    
    def get_friend(self, user_id):
        return self.friend_repository.get_friend(user_id)
    
    def create(self, friend):
        return self.friend_repository.create(friend)
    
    def delete(self, id):
        return self.friend_repository.delete(id)
    
    def delete_by_user_id_and_friend_user_id(self, user_id, friend_user_id):
        return self.friend_repository.delete_by_user_id_and_friend_user_id(user_id, friend_user_id)
    
    def is_friend(self, user_id, friend_user_id):
        return self.friend_repository.is_friend(user_id, friend_user_id)
    
    def get_friend_count(self, user_id):
        return self.friend_repository.get_friend_count(user_id)
    
    def get_friend_list_by_user_id(self, user_id):
        return self.friend_repository.get_friend_list_by_user_id(user_id)
    
    def get_friend_list_by_user_id_and_offset_and_limit(self, user_id, offset: int = 0, limit: int = 100):
        return self.friend_repository.get_friend_list_by_user_id_and_offset_and_limit(user_id, offset, limit) 
    
    def get_friend_list_by_user_id_and_offset_and_limit_and_keyword(self, user_id, offset: int = 0, limit: int = 100, keyword: str = ""):
        return self.friend_repository.get_friend_list_by_user_id_and_offset_and_limit_and_keyword(user_id, offset, limit, keyword)
