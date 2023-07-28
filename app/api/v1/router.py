from fastapi import APIRouter

from app.api.v1.endpoints import users, auth, profile, following, friend, friend_request, \
    video, tag

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/users", tags=["auth"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(profile.router, prefix="/profile", tags=["profile"])
api_router.include_router(following.router, prefix="/users", tags=["follow"])
api_router.include_router(friend.router, prefix="/users", tags=["friend"])
api_router.include_router(friend_request.router, prefix="/users", tags=["friend_request"])
api_router.include_router(video.router, prefix="/videos", tags=["video"])
api_router.include_router(tag.router, prefix="/tags", tags=["tag"])