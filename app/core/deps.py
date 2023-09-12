import logging
import uuid
import shutil
import os
from typing import Any

from fastapi import Depends, HTTPException, status, UploadFile
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from pydantic import ValidationError
from sqlalchemy.orm import Session
from moviepy.editor import VideoFileClip

from app import models, schemas, config
from app.core import security
from app.config import get_settings
from app.db.database import get_db_connection
from app.usecase.user_usecase import UserUseCase
from app.repositories.user_repository import UserRepository

logger = logging.getLogger(__name__)
env = get_settings()

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"api/users/login"
)
reusable_oauth2_optional = OAuth2PasswordBearer(
    tokenUrl=f"api/users/login", auto_error=False
)


def get_current_user(
    db: Session = Depends(get_db_connection),
    token: str = Depends(reusable_oauth2),
) -> models.User:
    try:
        payload = jwt.decode(
            token, env.SECRET_KEY, algorithms=[security.ALGORITHM]
        )
        token_data = schemas.TokenPayload(**payload)
    except (JWTError, ValidationError) as e:
        errmsg = str(e).replace('\n', ' ')
        logger.error(f"{type(e).__name__}: {errmsg}")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    user_usecase = UserUseCase(UserRepository(db))
    user = user_usecase.get(token_data.sub)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


def get_current_user_optional(
    db: Session = Depends(get_db_connection),
    token: str = Depends(reusable_oauth2_optional),
) -> Any:
    if not token:
        return None

    try:
        payload = jwt.decode(
            token, env.SECRET_KEY, algorithms=[security.ALGORITHM]
        )
        token_data = schemas.TokenPayload(**payload)
    except (JWTError, ValidationError) as e:
        errmsg = str(e).replace('\n', ' ')
        logger.error(f"{type(e).__name__}: {errmsg}")
        return None
    user_usecase = UserUseCase(UserRepository(db))
    user = user_usecase.get(token_data.sub)
    if not user:
        return None
    return user


def get_current_active_user(
    db: Session = Depends(get_db_connection),
    current_user: models.User = Depends(get_current_user),
) -> models.User:
    user_usecase = UserUseCase(UserRepository(db))
    if not user_usecase.is_active(current_user):
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


def get_current_active_superuser(
    db: Session = Depends(get_db_connection),
    current_user: models.User = Depends(get_current_user),
) -> models.User:
    user_usecase = UserUseCase(UserRepository(db))
    if not user_usecase.is_superuser(current_user):
        raise HTTPException(
            status_code=400, detail="The user doesn't have enough privileges"
        )
    return current_user


def upload_image(file: UploadFile, settings: config.Settings) -> Any:
    filename = file.filename
    file_size = file.file.seek(0, 2)
    logger.info(f"filename: {filename}, file_size: {file_size}")
    if file_size > settings.UPLOAD_IMAGE_SIZE_LIMIT:
        raise HTTPException(status_code=400, detail="File too large")
    
    content_type = file.content_type
    logger.info(f"content_type: {content_type}")
    if content_type not in settings.UPLOAD_IMAGE_TYPE:
        raise HTTPException(status_code=400, detail="Invalid file type")
    
    filename = f"{uuid.uuid4()}.{filename.split('.')[-1]}"
    file.file.seek(0)
    with open(f"{settings.UPLOAD_IMAGE_PATH}/{filename}", "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return f"{settings.UPLOAD_IMAGE_PATH}/{filename}"


def upload_video(file: UploadFile, settings: config.Settings) -> Any:
    filename = file.filename
    file_size = file.file.seek(0, 2)
    logger.info(f"filename: {filename}, file_size: {file_size}")
    if file_size > settings.UPLOAD_VIDEO_SIZE_LIMIT:
        raise HTTPException(status_code=400, detail="File too large")
    
    content_type = file.content_type
    logger.info(f"content_type: {content_type}")
    if content_type not in settings.UPLOAD_VIDEO_TYPE:
        raise HTTPException(status_code=400, detail="Invalid file type")
    
    filename = f"{uuid.uuid4()}.{filename.split('.')[-1]}"
    file.file.seek(0)
    with open(f"{settings.UPLOAD_VIDEO_PATH}/{filename}", "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return f"{settings.UPLOAD_VIDEO_PATH}/{filename}"


def generate_video_thumbnails(settings: config.Settings, video_path, file_id, num_thumbnails: int = 12):
    # origin_path = os.path.join(settings.UPLOAD_VIDEO_PATH, video_path)
    try:
        origin_path = video_path
        clip = VideoFileClip(origin_path)
        duration = clip.duration
        interval = duration / num_thumbnails
        thumbnails = []

        thumbnail_relate_path = os.path.join(settings.UPLOAD_VIDEO_PATH, f"thumbnails/{file_id}")
        os.makedirs(thumbnail_relate_path, exist_ok=True)
        for i in range(num_thumbnails):
            time = i * interval
            thumbnail_path = os.path.join(thumbnail_relate_path, f"thumbnails_{i}.jpg")
            thumbnail = clip.save_frame(thumbnail_path, time)
            thumbnails.append(thumbnail)

        clip.close()

        return True
    except Exception as e:
        logger.error(f"{type(e).__name__}: {str(e)}")
        return False