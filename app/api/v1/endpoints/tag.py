import logging
import uuid
from typing import Any, Annotated

from fastapi import APIRouter, Body, Depends, File, Form, UploadFile
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session

from app import schemas, models, config
from app.usecase.tag_usecase import TagUseCase
from app.repositories.tag_repository import TagRepository
from app.config import get_settings
from app.db.database import get_db_connection
from app.core.deps import get_current_user


logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/")
def get_tag(
    page: int = 1,
    limit: int = 30,
    keyword: str = '',
    db: Session = Depends(get_db_connection),
) -> Any:
    """
    Get tag list by offset and limit and keyword.
    """
    tag_usecase = TagUseCase(TagRepository(db))
    if keyword != '':
        data = tag_usecase.get_tag_list_by_offset_and_limit_and_keyword((page - 1) * limit, limit, keyword)
        count = tag_usecase.get_tag_list_by_offset_and_limit_and_keyword_count(keyword)
    else:
        data = tag_usecase.get_tag_list_by_offset_and_limit((page - 1) * limit, limit)
        count = tag_usecase.get_tag_list_by_offset_and_limit_count()

    response_data = [schemas.TagResponse(
        id=tag.id,
        name=tag.name,
        slug=tag.slug,
    ) for tag in data]
    return {
        'data': response_data,
        'page': page,
        'count': count,
    }


@router.post("/", response_model=schemas.TagResponse)
def create_tag(
    obj_in: schemas.TagCreate,
    db: Session = Depends(get_db_connection),
    current_user: models.User = Depends(get_current_user),
) -> Any:
    """
    Create a tag.
    """
    tag_usecase = TagUseCase(TagRepository(db))
    tag = tag_usecase.create(obj_in)
    return schemas.TagResponse(
        id=tag.id,
        name=tag.name,
        slug=tag.slug,
    )


@router.delete("/{id}")
def delete_tag(
    id: uuid.UUID,
    db: Session = Depends(get_db_connection),
    current_user: models.User = Depends(get_current_user),
) -> Any:
    """
    Delete a tag.
    """
    tag_usecase = TagUseCase(TagRepository(db))
    tag = tag_usecase.get(id)
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    tag = tag_usecase.delete(id)
    return None