from fastapi import APIRouter

from app.api.v1.endpoints import users, auth, profile, following

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/users", tags=["auth"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(profile.router, prefix="/profile", tags=["profile"])
api_router.include_router(following.router, prefix="/users", tags=["follow"])