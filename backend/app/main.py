from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import (
    create_postgres, delete_postgres,
    create_minio, delete_minio,
    create_qdrant, delete_qdrant,
    fill_test_data
)
from app.router import router_health, router_image, router_images
from app.config import settings

@asynccontextmanager
async def lifespan(app: FastAPI):
    if settings.APP_MODE == 'DEV':
        await delete_postgres()
        await delete_minio()
        await delete_qdrant()
        print('База очищена')
    await create_postgres()
    await create_minio()
    await create_qdrant()
    print('База готова к работе')
    if settings.APP_MODE == 'DEV':
        await fill_test_data()
        print('База заполнена тестовыми данными')
    yield
    print('Выключение')


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
