from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, DateTime, func
from app.config import settings


class Model(DeclarativeBase):
    pass


class ImageOrm(Model):
    __tablename__ = 'images'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, index=True)
    image_object_name: Mapped[str]
    thumbnail_object_name: Mapped[str]
    embedding_vector_id: Mapped[str]
    uploaded_at: Mapped[DateTime] = mapped_column(DateTime, default=func.now())
    size: Mapped[int]
    
    @staticmethod
    def minio_link(object_name: str):
        return f'{settings.MINIO_BUCKET_URL}/{object_name}'
