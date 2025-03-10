import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.database import create_tables, create_media_folders
from app.router import router_health, router_image, router_images
from app.config import settings

@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_tables()
    await create_media_folders()
    print('База данных и медиа-файлы подготовлены')
    yield

print(f'Starting server on {settings.BACKEND_HOST}:{settings.BACKEND_PORT}')
app = FastAPI(title='Smart Gallery - backend', description='', lifespan=lifespan)

app.include_router(router_health)
app.include_router(router_image)
app.include_router(router_images)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/storage", StaticFiles(directory=settings.MEDIA_FOLDER), name="storage")
