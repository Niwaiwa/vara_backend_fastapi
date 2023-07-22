from app.repositories.following_repository import FollowingRepository


class FollowingUseCase:
    following_repository: FollowingRepository

    def __init__(self, following_repository: FollowingRepository) -> None:
        self.following_repository = following_repository

    def get(self, id):
        return self.following_repository.get(id)
    
    def get_multi(self, skip: int = 0, limit: int = 100):
        return self.following_repository.get_multi(skip, limit)
    
    def get_following(self, user_id):
        return self.following_repository.get_following(user_id)
    
    def create(self, following):
        return self.following_repository.create(following)
    
    def delete(self, id):
        return self.following_repository.delete(id)
    
    def delete_by_user_id_and_following_user_id(self, user_id, following_user_id):
        return self.following_repository.delete_by_user_id_and_following_user_id(user_id, following_user_id)
    
    def is_following(self, user_id, following_user_id):
        return self.following_repository.is_following(user_id, following_user_id)
    
    def get_following_count(self, user_id):
        return self.following_repository.get_following_count(user_id)
    
    def get_follower_count(self, following_user_id):
        return self.following_repository.get_follower_count(following_user_id)
    
    def get_following_list_by_user_id(self, user_id):
        return self.following_repository.get_following_list_by_user_id(user_id)
    
    def get_follower_list_by_user_id(self, user_id):
        return self.following_repository.get_follower_list_by_user_id(user_id)
    
    def get_following_list_by_user_id_and_offset_and_limit(self, user_id, offset: int = 0, limit: int = 100):
        return self.following_repository.get_following_list_by_user_id_and_offset_and_limit(user_id, offset, limit) 
    
    def get_follower_list_by_user_id_and_offset_and_limit(self, user_id, offset: int = 0, limit: int = 100):
        return self.following_repository.get_follower_list_by_user_id_and_offset_and_limit(user_id, offset, limit)
