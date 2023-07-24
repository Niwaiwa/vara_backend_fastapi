from app.repositories.friend_request_repository import FriendRequestRepository


class FriendRequestUseCase:

    def __init__(self, friend_request_repository: FriendRequestRepository) -> None:
        self.friend_request_repository = friend_request_repository

    def get(self, id):
        return self.friend_request_repository.get(id)
    
    def get_multi(self, skip: int = 0, limit: int = 100):
        return self.friend_request_repository.get_multi(skip, limit)
    
    def get_friend_request(self, from_user_id, to_user_id):
        return self.friend_request_repository.get_friend_request(from_user_id, to_user_id)
    
    def create(self, friend_request):
        return self.friend_request_repository.create(friend_request)
    
    def delete(self, id):
        return self.friend_request_repository.delete(id)
    
    def delete_by_from_user_id_and_to_user_id(self, from_user_id, to_user_id):
        return self.friend_request_repository.delete_by_from_user_id_and_to_user_id(from_user_id, to_user_id)
    
    def is_friend_request(self, from_user_id, to_user_id):
        return self.friend_request_repository.is_friend_request(from_user_id, to_user_id)
    
    def get_friend_request_count_by_from_user_id(self, from_user_id):
        return self.friend_request_repository.get_friend_request_count_by_from_user_id(from_user_id)

    def get_friend_request_count_by_to_user_id(self, to_user_id):
        return self.friend_request_repository.get_friend_request_count_by_to_user_id(to_user_id)

    def get_friend_request_list_by_from_user_id(self, from_user_id):
        return self.friend_request_repository.get_friend_request_list_by_from_user_id(from_user_id)
    
    def get_friend_request_list_by_from_user_id_and_offset_and_limit(self, from_user_id, offset: int = 0, limit: int = 100):
        return self.friend_request_repository.get_friend_request_list_by_from_user_id_and_offset_and_limit(from_user_id, offset, limit) 
    
    def get_friend_request_list_by_from_user_id_and_offset_and_limit_and_keyword(self, from_user_id, offset: int = 0, limit: int = 100, keyword: str = ""):
        return self.friend_request_repository.get_friend_request_list_by_from_user_id_and_offset_and_limit_and_keyword(from_user_id, offset, limit, keyword)
    
    def get_friend_request_list_by_to_user_id(self, to_user_id):
        return self.friend_request_repository.get_friend_request_list_by_to_user_id(to_user_id)
    
    def get_friend_request_list_by_to_user_id_and_offset_and_limit(self, to_user_id, offset: int = 0, limit: int = 100):
        return self.friend_request_repository.get_friend_request_list_by_to_user_id_and_offset_and_limit(to_user_id, offset, limit)
    
    def get_friend_request_list_by_to_user_id_and_offset_and_limit_and_keyword(self, to_user_id, offset: int = 0, limit: int = 100, keyword: str = ""):
        return self.friend_request_repository.get_friend_request_list_by_to_user_id_and_offset_and_limit_and_keyword(to_user_id, offset, limit, keyword)
    
