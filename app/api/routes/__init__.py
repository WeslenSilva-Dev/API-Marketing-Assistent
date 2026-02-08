from fastapi import APIRouter

from .content import router as content_router
from .instagram import router as instagram_router

api_router = APIRouter()

api_router.include_router(content_router, prefix="/content", tags=["Conteúdo"])
api_router.include_router(instagram_router, prefix="/instagram", tags=["Instagram"])

__all__ = ["api_router"]
