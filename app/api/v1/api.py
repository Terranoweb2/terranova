from fastapi import APIRouter

from app.api.v1.endpoints import (
    auth,
    users,
    text,
    images,
    music,
    documents,
    admin
)

api_router = APIRouter()

# Authentication
api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])

# User management
api_router.include_router(users.router, prefix="/users", tags=["users"])

# AI Services
api_router.include_router(text.router, prefix="/text", tags=["text"])
api_router.include_router(images.router, prefix="/images", tags=["images"])
api_router.include_router(music.router, prefix="/music", tags=["music"])
api_router.include_router(documents.router, prefix="/documents", tags=["documents"])

# Admin
api_router.include_router(admin.router, prefix="/admin", tags=["admin"])
