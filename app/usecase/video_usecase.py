from app.core.security import get_password_hash, verify_password
from app.repositories.video_repository import VideoRepository


class VideoUseCase:
    videoRepository: VideoRepository

    def __init__(self, videoRepository: VideoRepository) -> None:
        self.videoRepository = videoRepository

    def create(self, video, tags):
        return self.videoRepository.create(video, tags)

    def get(self, id):
        return self.videoRepository.get(id)

    def get_multi(self, skip: int = 0, limit: int = 100):
        return self.videoRepository.get_multi(skip, limit)

    def update(self, id, video, tags):
        return self.videoRepository.update(id, video, tags)

    def delete(self, id):
        return self.videoRepository.delete(id)

    def get_video_count(self, user_id):
        return self.videoRepository.get_video_count(user_id)

    def get_video_list_by_user_id(self, user_id):
        return self.videoRepository.get_video_list_by_user_id(user_id)

    def get_video_list_by_user_id_and_offset_and_limit(self, user_id, offset: int = 0, limit: int = 100):
        return self.videoRepository.get_video_list_by_user_id_and_offset_and_limit(user_id, offset, limit)

    def get_video_list_by_user_id_and_offset_and_limit_and_rating(self, user_id, offset: int = 0, limit: int = 100, rating: str = 'G'):
        return self.videoRepository.get_video_list_by_user_id_and_offset_and_limit_and_rating(user_id, offset, limit, rating)

    def get_video_list_by_offset_and_limit(self, offset: int = 0, limit: int = 100):
        return self.videoRepository.get_video_list_by_offset_and_limit(offset, limit)

    def get_video_list_by_offset_and_limit_and_rating(self, offset: int = 0, limit: int = 100, rating: str = 'G'):
        return self.videoRepository.get_video_list_by_offset_and_limit_and_rating(offset, limit, rating)
    
    def get_video_list_by_offset_and_limit_and_rating_count(self, offset: int = 0, limit: int = 100, rating: str = 'G'):
        return self.videoRepository.get_video_list_by_offset_and_limit_and_rating_count(offset, limit, rating)

    def get_video_list_by_offset_and_limit_and_keyword(self, offset: int = 0, limit: int = 100, keyword: str = ''):
        return self.videoRepository.get_video_list_by_offset_and_limit_and_keyword(offset, limit, keyword)
    
    def get_video_list_by_offset_and_limit_and_rating_and_keyword(self, offset: int = 0, limit: int = 100, rating: str = 'G', keyword: str = ''):
        return self.videoRepository.get_video_list_by_offset_and_limit_and_rating_and_keyword(offset, limit, rating, keyword)

    def get_video_list_by_offset_and_limit_and_rating_and_keyword_count(self, offset: int = 0, limit: int = 100, rating: str = 'G', keyword: str = ''):
        return self.videoRepository.get_video_list_by_offset_and_limit_and_rating_and_keyword_count(offset, limit, rating, keyword)

    def get_video_list_by_offset_and_limit_and_tag(self, offset: int = 0, limit: int = 100, tag: str = ''):
        return self.videoRepository.get_video_list_by_offset_and_limit_and_tag(offset, limit, tag)
    
    def get_video_list_by_offset_and_limit_and_rating_and_tag(self, offset: int = 0, limit: int = 100, rating: str = 'G', tag: str = ''):
        return self.videoRepository.get_video_list_by_offset_and_limit_and_rating_and_tag(offset, limit, rating, tag)

    def get_video_list_by_offset_and_limit_and_rating_and_tag_count(self, offset: int = 0, limit: int = 100, rating: str = 'G', tag: str = ''):
        return self.videoRepository.get_video_list_by_offset_and_limit_and_rating_and_tag_count(offset, limit, rating, tag)
