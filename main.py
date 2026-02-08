"""
Ponto de entrada da API - FastAPI.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.api.routes import api_router

app = FastAPI(
    title=settings.app_name,
    description="API para gerar conteúdo (imagem + legenda) com DALL-E e ChatGPT e publicar no Instagram.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api")


@app.get("/")
def root():
    return {
        "message": "Instagram Content API",
        "docs": "/docs",
        "api": "/api",
    }


@app.get("/health")
def health():
    return {"status": "ok"}
