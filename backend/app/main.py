from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from database import create_tables, delete_tables, create_media_folders, delete_media_folders
from router import router_image ,router_images
from config import settings


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
    allow_methods=['*'],
    allow_headers=['*'],
)


if __name__ == '__main__':
    uvicorn.run('main:app', host=settings.HOST, port=settings.PORT, reload=True, reload_dirs=['app'])
