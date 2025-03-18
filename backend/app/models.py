from sqlalchemy import DateTime, Integer, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from app.config import settings


class Model(DeclarativeBase):
    """Базовая модель для декларативного объявления ORM."""
    pass


class ImageOrm(Model):
    """Модель изображения в базе данных."""

    __tablename__ = "images"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, index=True)
    image_object_name: Mapped[str]
    thumbnail_object_name: Mapped[str]
    embedding_vector_id: Mapped[str]
    uploaded_at: Mapped[DateTime] = mapped_column(DateTime, default=func.now())
    size: Mapped[int]

    @staticmethod
    def minio_link(object_name: str) -> str:
        """
        Генерирует URL для объекта MinIO.

        :param object_name: Имя объекта в MinIO.
        :return: Полный URL объекта в MinIO.
        """
        return f"{settings.MINIO_BUCKET_URL}/{object_name}"
