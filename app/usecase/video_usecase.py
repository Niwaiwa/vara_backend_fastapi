import uuid
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

    def get_video_list_by_offset_and_limit_and_rating(self, offset: int = 0, limit: int = 100, rating: str = 'G'):
        return self.videoRepository.get_video_list_by_offset_and_limit_and_rating(offset, limit, rating)
    
    def get_video_list_by_offset_and_limit_and_rating_count(self, rating: str = 'G'):
        return self.videoRepository.get_video_list_by_offset_and_limit_and_rating_count(rating)

    def get_video_list_by_offset_and_limit_and_rating_and_keyword(self, offset: int = 0, limit: int = 100, rating: str = 'G', keyword: str = ''):
        return self.videoRepository.get_video_list_by_offset_and_limit_and_rating_and_keyword(offset, limit, rating, keyword)

    def get_video_list_by_offset_and_limit_and_rating_and_keyword_count(self, rating: str = 'G', keyword: str = ''):
        return self.videoRepository.get_video_list_by_offset_and_limit_and_rating_and_keyword_count(rating, keyword)

    def get_video_list_by_offset_and_limit_and_rating_and_tag(self, offset: int = 0, limit: int = 100, rating: str = 'G', tag: str = ''):
        return self.videoRepository.get_video_list_by_offset_and_limit_and_rating_and_tag(offset, limit, rating, tag)

    def get_video_list_by_offset_and_limit_and_rating_and_tag_count(self, rating: str = 'G', tag: str = ''):
        return self.videoRepository.get_video_list_by_offset_and_limit_and_rating_and_tag_count(rating, tag)

    def get_video_list_by_offset_and_limit_and_rating_and_tags(self, offset: int = 0, limit: int = 100, rating: str = 'G', tags: list = []):
        return self.videoRepository.get_video_list_by_offset_and_limit_and_rating_and_tags(offset, limit, rating, tags)

    def get_video_list_by_offset_and_limit_and_rating_and_tags_count(self, rating: str = 'G', tags: list = []):
        return self.videoRepository.get_video_list_by_offset_and_limit_and_rating_and_tags_count(rating, tags)
    
    def get_video_list_by_offset_and_limit_and_rating_and_tags_and_user_id_and_sort(
            self, offset: int = 0, limit: int = 100, rating: str = 'G', tags: list = [], sort: str = 'latest', user_id: uuid.UUID | str = ''):
        if sort == 'oldest':
            return self.videoRepository.get_video_list_by_offset_and_limit_and_rating_and_tags_and_user_id_and_sort_oldest(offset, limit, rating, tags, user_id)
        elif sort == 'views':
            return self.videoRepository.get_video_list_by_offset_and_limit_and_rating_and_tags_and_user_id_and_sort_views(offset, limit, rating, tags, user_id)
        elif sort == 'likes':
            return self.videoRepository.get_video_list_by_offset_and_limit_and_rating_and_tags_and_user_id_and_sort_likes(offset, limit, rating, tags, user_id)
        else:
            return self.videoRepository.get_video_list_by_offset_and_limit_and_rating_and_tags_and_user_id_and_sort_latest(offset, limit, rating, tags, user_id)
        
    def get_video_list_by_offset_and_limit_and_rating_and_tags_and_user_id_and_sort_count(
            self, rating: str = 'G', tags: list = [], sort: str = 'latest', user_id: uuid.UUID | str = ''):
        if sort == 'oldest':
            return self.videoRepository.get_video_list_by_offset_and_limit_and_rating_and_tags_and_user_id_and_sort_oldest_count(rating, tags, user_id)
        elif sort == 'views':
            return self.videoRepository.get_video_list_by_offset_and_limit_and_rating_and_tags_and_user_id_and_sort_views_count(rating, tags, user_id)
        elif sort == 'likes':
            return self.videoRepository.get_video_list_by_offset_and_limit_and_rating_and_tags_and_user_id_and_sort_likes_count(rating, tags, user_id)
        else:
            return self.videoRepository.get_video_list_by_offset_and_limit_and_rating_and_tags_and_user_id_and_sort_latest_count(rating, tags, user_id)

    def is_video_liked(self, user_id, video_id):
        return self.videoRepository.is_video_liked(user_id, video_id)

    def like_video(self, user_id, video_id):
        return self.videoRepository.like_video(user_id, video_id)
    
    def unlike_video(self, user_id, video_id):
        return self.videoRepository.unlike_video(user_id, video_id)