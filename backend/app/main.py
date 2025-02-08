from contextlib import asynccontextmanager

from fastapi import FastAPI
import uvicorn

from database import create_tables, delete_tables, create_media_folders, delete_media_folders
from router import router_image ,router_images


# потом удалить даже не понимаю зач надо
@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_tables()
    await create_media_folders()
    print("База готова")
    yield
    await delete_tables()
    await delete_media_folders()
    print("База очищена")


app = FastAPI(lifespan=lifespan)

app.include_router(router_image)
app.include_router(router_images)

if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8000, reload=True, reload_dirs=['app'])
