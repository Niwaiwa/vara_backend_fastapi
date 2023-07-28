import uuid
from typing import Any, Dict, Optional

from sqlalchemy.orm import Session

from app.models.user_model import User
from app.models.video_model import Video
from app.models.tag_model import Tag
from app.repositories.base_repository import BaseRepository
from app.schemas.tag_schema import TagCreate, TagUpdate


class TagRepository(BaseRepository[Tag, TagCreate, TagUpdate]):

    def __init__(self, db: Session):
        super().__init__(Tag, db)

    def get(self, id: Any) -> Optional[Tag]:
        return self.db.query(Tag).filter(Tag.id == id).first()

    def get_multi(self, skip: int = 0, limit: int = 100) -> list:
        return self.db.query(Tag).offset(skip).limit(limit).all()

    def get_by_name(self, name: str) -> Optional[Tag]:
        return self.db.query(Tag).filter(Tag.name == name).first()

    def create(self, obj_in: TagCreate) -> Tag:
        db_obj = Tag(name=obj_in.name, slug=obj_in.slug)
        self.db.add(db_obj)
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj

    def update(self, id: uuid.UUID, obj_in: TagUpdate) -> Tag:
        obj = self.db.query(Tag).get(id)
        obj_in_data: Dict[str, Any] = obj_in.dict()
        for field in obj_in_data:
            if field in obj_in_data:
                setattr(obj, field, obj_in_data[field])
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def delete(self, id: uuid.UUID) -> Tag:
        obj = self.db.query(Tag).get(id)
        self.db.delete(obj)
        self.db.commit()
        return obj
    
    def get_tag_list_by_offset_and_limit(self, offset: int = 0, limit: int = 100):
        return self.db.query(Tag).order_by(Tag.name).offset(offset).limit(limit).all()
    
    def get_tag_list_by_offset_and_limit_count(self):
        return self.db.query(Tag).count()

    def get_tag_list_by_offset_and_limit_and_keyword(self, offset: int = 0, limit: int = 100, keyword: str = ''):
        return self.db.query(Tag).filter(Tag.name.like('%' + keyword + '%')).order_by(Tag.name).offset(offset).limit(limit).all()
    
    def get_tag_list_by_offset_and_limit_and_keyword_count(self, keyword: str = ''):
        return self.db.query(Tag).filter(Tag.name.like('%' + keyword + '%')).count()