import logging
import uuid
from typing import Any, Annotated

from fastapi import APIRouter, Body, Depends, File, Form, UploadFile, Query
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session

from app import schemas, models, config
from app.usecase.user_usecase import UserUseCase
from app.usecase.video_usecase import VideoUseCase
from app.repositories.user_repository import UserRepository
from app.repositories.video_repository import VideoRepository
from app.config import get_settings
from app.db.database import get_db_connection
from app.core.deps import get_current_user, get_current_user_optional, upload_video, generate_video_thumbnails

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("")
def get_video(
    page: int = 1,
    limit: int = 30,
    rating: str = 'G',
    sort: str = 'latest',
    tags: list[str] = Query(None, alias='tag'),
    user_id: uuid.UUID = Query('', alias='user'),
    db: Session = Depends(get_db_connection),
) -> Any:
    """
    Get a specific video by id.
    """
    if user_id:
        user_usecase = UserUseCase(UserRepository(db))
        user = user_usecase.get(user_id)
        if not user:
            return {
                'data': [],
                'page': page,
                'count': 0,
            }

    if rating not in ['G', 'E', 'All', 'all']:
        rating = 'G'
    elif rating == 'All' or rating == 'all':
        rating = ''

    video_usecase = VideoUseCase(VideoRepository(db))
    data = video_usecase.get_video_list_by_offset_and_limit_and_rating_and_tags_and_user_id_and_sort(
        (page - 1) * limit,
        limit,
        rating,
        tags,
        sort,
        user_id,
    )
    count = video_usecase.get_video_list_by_offset_and_limit_and_rating_and_tags_and_user_id_and_sort_count(
        rating,
        tags,
        sort,
        user_id,
    )

    response_data = [schemas.VideoResponse(
        id=video.id,
        user=schemas.ContentUser(
            username=video.user.username,
            nickname=video.user.nickname,
            avatar=video.user.avatar,
            is_following=False,
        ),
        title=video.title,
        description=video.description,
        video_file=video.video_file,
        video_url=video.video_url,
        views_count=video.views_count,
        likes_count=video.likes_count,
        created_at=video.created_at,
        updated_at=video.updated_at,
        tags=video.tags,
        rating=video.rating,
    ) for video in data]
    return {
        'data': response_data,
        'page': page,
        'count': count,
    }


@router.get("/{video_id}", response_model=schemas.VideoResponse)
def get_video_by_id(
    video_id: uuid.UUID,
    db: Session = Depends(get_db_connection),
    current_user: models.User = Depends(get_current_user_optional),
) -> Any:
    """
    Get a specific video by id.
    """
    video_usecase = VideoUseCase(VideoRepository(db))
    video = video_usecase.get(video_id)
    if not video:
        raise HTTPException(status_code=404, detail="Video not found")

    is_liked = False
    if current_user:
        is_liked = video_usecase.is_video_liked(current_user.id, video.id)

    response_data = schemas.VideoResponse(
        id=video.id,
        user=schemas.ContentUser(
            username=video.user.username,
            nickname=video.user.nickname,
            avatar=video.user.avatar,
            is_following=False,
        ),
        title=video.title,
        description=video.description,
        video_file=video.video_file,
        video_url=video.video_url,
        views_count=video.views_count,
        likes_count=video.likes_count,
        created_at=video.created_at,
        updated_at=video.updated_at,
        tags=video.tags,
        rating=video.rating,
        is_liked=is_liked,
    )
    return response_data


@router.post("", response_model=schemas.VideoResponse)
def create_video(
    title: Annotated[str, Form(...)],
    description: Annotated[str, Form(...)],
    rating: Annotated[str, Form(...)],   
    video_file: Annotated[UploadFile | None, File()] = None,
    video_url: Annotated[str | None, Form()] = None,
    tags: Annotated[list[str] | None, Form()] = None,
    db: Session = Depends(get_db_connection),
    current_user: models.User = Depends(get_current_user),
    settings: config.Settings = Depends(get_settings),
) -> Any:
    """
    Create a video.
    """
    video_filename = None

    if not video_url and not video_file:
        raise HTTPException(status_code=400, detail="video_url or video_file is required")

    if video_file:
        video_filename = upload_video(video_file, settings)

    if rating not in ['G', 'E']:
        raise HTTPException(status_code=400, detail="Invalid rating")

    video_usecase = VideoUseCase(VideoRepository(db))
    video_create_data = schemas.VideoCreate(
        user_id=current_user.id,
        title=title,
        description=description,
        video_file=video_filename,
        video_url=video_url,
        rating=rating,
    )

    video = video_usecase.create(
        video_create_data,
        tags,
    )

    thumbnail_result = generate_video_thumbnails(settings, video.video_file, video.id)
    if thumbnail_result:
        logger.info(f"thumbnail_result: {thumbnail_result}")

    return schemas.VideoResponse(
        id=video.id,
        user=schemas.ContentUser(
            username=video.user.username,
            nickname=video.user.nickname,
            avatar=video.user.avatar,
            is_following=False,
        ),
        title=video.title,
        description=video.description,
        video_file=video.video_file,
        video_url=video.video_url,
        views_count=video.views_count,
        likes_count=video.likes_count,
        created_at=video.created_at,
        updated_at=video.updated_at,
        tags=video.tags,
        rating=video.rating,
    )


@router.put("/{video_id}", response_model=schemas.VideoResponse)
def update_video(
    video_id: uuid.UUID,
    update_data: schemas.VideoUpdate,
    db: Session = Depends(get_db_connection),
    current_user: models.User = Depends(get_current_user),
) -> Any:
    """
    Update a video.
    """
    video_usecase = VideoUseCase(VideoRepository(db))
    video = video_usecase.get(video_id)
    if not video:
        raise HTTPException(status_code=404, detail="Video not found")

    tags = update_data.tags
    update_data.tags = None
    video_update_data = update_data.dict(exclude_unset=True)

    video = video_usecase.update(
        video_id,
        video_update_data,
        tags,
    )

    return schemas.VideoResponse(
        id=video.id,
        user=schemas.ContentUser(
            username=video.user.username,
            nickname=video.user.nickname,
            avatar=video.user.avatar,
            is_following=False,
        ),
        title=video.title,
        description=video.description,
        video_file=video.video_file,
        video_url=video.video_url,
        views_count=video.views_count,
        likes_count=video.likes_count,
        created_at=video.created_at,
        updated_at=video.updated_at,
        tags=video.tags,
        rating=video.rating,
    )


@router.delete("/{video_id}")
def delete_video(
    video_id: uuid.UUID,
    db: Session = Depends(get_db_connection),
    current_user: models.User = Depends(get_current_user),
) -> Any:
    """
    Delete a video.
    """
    video_usecase = VideoUseCase(VideoRepository(db))
    video = video_usecase.get(video_id)
    if not video:
        raise HTTPException(status_code=404, detail="Video not found")

    video_usecase.delete(video_id)

    return None


@router.post("/{video_id}/like", response_model=schemas.VideoResponse)
def like_video(
    video_id: uuid.UUID,
    db: Session = Depends(get_db_connection),
    current_user: models.User = Depends(get_current_user),
) -> Any:
    """
    Like a video.
    """
    video_usecase = VideoUseCase(VideoRepository(db))
    video = video_usecase.get(video_id)
    if not video:
        raise HTTPException(status_code=404, detail="Video not found")

    is_liked = video_usecase.is_video_liked(current_user.id, video.id)
    if is_liked:
        raise HTTPException(status_code=400, detail="Already liked")

    video_usecase.like_video(current_user.id, video_id)

    return schemas.VideoResponse(
        id=video.id,
        user=schemas.ContentUser(
            username=video.user.username,
            nickname=video.user.nickname,
            avatar=video.user.avatar,
            is_following=False,
        ),
        title=video.title,
        description=video.description,
        video_file=video.video_file,
        video_url=video.video_url,
        views_count=video.views_count,
        likes_count=video.likes_count,
        created_at=video.created_at,
        updated_at=video.updated_at,
        tags=video.tags,
        rating=video.rating,
        is_liked=True,
    )


@router.post("/{video_id}/unlike", response_model=schemas.VideoResponse)
def unlike_video(
    video_id: uuid.UUID,
    db: Session = Depends(get_db_connection),
    current_user: models.User = Depends(get_current_user),
) -> Any:
    """
    Unlike a video.
    """
    video_usecase = VideoUseCase(VideoRepository(db))
    video = video_usecase.get(video_id)
    if not video:
        raise HTTPException(status_code=404, detail="Video not found")

    is_liked = video_usecase.is_video_liked(current_user.id, video.id)
    if not is_liked:
        raise HTTPException(status_code=400, detail="Not liked yet")

    video_usecase.unlike_video(current_user.id, video_id)

    return schemas.VideoResponse(
        id=video.id,
        user=schemas.ContentUser(
            username=video.user.username,
            nickname=video.user.nickname,
            avatar=video.user.avatar,
            is_following=False,
        ),
        title=video.title,
        description=video.description,
        video_file=video.video_file,
        video_url=video.video_url,
        views_count=video.views_count,
        likes_count=video.likes_count,
        created_at=video.created_at,
        updated_at=video.updated_at,
        tags=video.tags,
        rating=video.rating,
    )