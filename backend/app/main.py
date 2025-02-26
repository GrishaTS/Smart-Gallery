import os
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.database import create_tables, delete_tables, create_media_folders, delete_media_folders
from app.router import router_image ,router_images
from app.config import settings


# потом удалить даже не понимаю зач надо
@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_tables()
    await create_media_folders()
    print('База готова')
    yield
    await delete_tables()
    await delete_media_folders()
    print('База очищена')

app = FastAPI(lifespan=lifespan)

app.include_router(router_image)
app.include_router(router_images)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.UI_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

os.makedirs(settings.MEDIA_FOLDER, exist_ok=True)
app.mount("/storage", StaticFiles(directory=settings.MEDIA_FOLDER), name="storage")
