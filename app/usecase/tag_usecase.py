from app.repositories.tag_repository import TagRepository


class TagUseCase:
    tagRepository: TagRepository

    def __init__(self, tagRepository: TagRepository) -> None:
        self.tagRepository = tagRepository

    def create(self, tag):
        existing_tag = self.tagRepository.get_by_name(tag.name)
        if existing_tag:
            return existing_tag

        slug = tag.name.lower().replace(' ', '-')
        tag.slug = slug
        return self.tagRepository.create(tag)

    def get(self, id):
        return self.tagRepository.get(id)

    def get_multi(self, skip: int = 0, limit: int = 100):
        return self.tagRepository.get_multi(skip, limit)

    def update(self, id, tag):
        return self.tagRepository.update(id, tag)

    def delete(self, id):
        return self.tagRepository.delete(id)
    
    def get_tag_list_by_offset_and_limit(self, offset: int = 0, limit: int = 100):
        return self.tagRepository.get_tag_list_by_offset_and_limit(offset, limit)
    
    def get_tag_list_by_offset_and_limit_count(self):
        return self.tagRepository.get_tag_list_by_offset_and_limit_count()
    
    def get_tag_list_by_offset_and_limit_and_keyword(self, offset: int = 0, limit: int = 100, keyword: str = ''):
        return self.tagRepository.get_tag_list_by_offset_and_limit_and_keyword(offset, limit, keyword)
    
    def get_tag_list_by_offset_and_limit_and_keyword_count(self, keyword: str = ''):
        return self.tagRepository.get_tag_list_by_offset_and_limit_and_keyword_count(keyword)