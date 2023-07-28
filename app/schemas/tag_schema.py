import uuid, datetime
from typing import Optional

from pydantic import BaseModel


class TagBase(BaseModel):
    name: str


class TagCreate(TagBase):
    pass


class TagUpdate(TagBase):
    pass


class TagInDBBase(TagBase):
    id: Optional[uuid.UUID] = None
    slug: Optional[str] = None

    class Config:
        orm_mode = True


class Tag(TagInDBBase):
    pass


class TagResponse(BaseModel):
    id: Optional[uuid.UUID] = None
    name: Optional[str] = None
    slug: Optional[str] = None


class TagListResponse(BaseModel):
    tag_list: list[TagResponse] = []
    page: int
    count: int
