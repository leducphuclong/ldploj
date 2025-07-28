from fastapi import APIRouter
from .endpoints import feed, auth

api_router = APIRouter()
api_router.include_router(feed.router, prefix="/feed", tags=["Feed"])
api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])