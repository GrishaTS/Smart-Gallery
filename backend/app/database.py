import os
import shutil
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy import Integer, DateTime, func
from app.config import settings

engine = create_async_engine(settings.POSTGRES_URL)
new_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


class Model(DeclarativeBase):
    pass


class ImageOrm(Model):
    __tablename__ = 'images'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, index=True)
    image_path: Mapped[str]
    preview_path: Mapped[str]
    embedding_path: Mapped[str]
    uploaded_at: Mapped[str] = mapped_column(DateTime, default=func.now())
    size: Mapped[int]


async def create_tables() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.create_all)


async def delete_tables() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.drop_all)


async def create_media_folders() -> None:
    for path in [settings.MEDIA_FOLDER, settings.IMAGES_PATH, settings.THUMBNAILS_PATH, settings.EMBEDDINGS_PATH]:
        os.makedirs(path, exist_ok=True)


async def delete_media_folders() -> None:
    if os.path.exists(settings.MEDIA_FOLDER):
        shutil.rmtree(settings.MEDIA_FOLDER)
