from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.router import router_health, router_embed
from app.config import settings


print(f'Starting server on {settings.BACKEND_HOST}:{settings.BACKEND_PORT}')
app = FastAPI(title="Smart Gallery - ml-api", description="Сервис для генерации эмбеддингов")

app.include_router(router_health)
app.include_router(router_embed)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.BACKEND_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
