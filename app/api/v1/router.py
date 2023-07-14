from fastapi import APIRouter

from app.api.v1.endpoints import users

api_router = APIRouter()
# api_router.include_router(auth.router, prefix="/users", tags=["auth"])
api_router.include_router(users.router, prefix="/users", tags=["users"])