import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import create_db, create_minio, delete_db, delete_minio
from app.router import router_health, router_image, router_images
from app.config import settings

@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_db()
    await create_minio()
    yield
    await delete_db()
    await delete_minio()


print(f'Starting server on {settings.BACKEND_HOST}:{settings.BACKEND_PORT}')
app = FastAPI(title='Smart Gallery - backend', lifespan=lifespan)

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
