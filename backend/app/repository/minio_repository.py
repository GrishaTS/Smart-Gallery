from io import BytesIO

from PIL import Image
from fastapi import HTTPException
from minio import S3Error

from app.config import settings
from app.database.minio_client import minio_client
from app.repository.base_repository import BaseRepository


class MinioRepository(BaseRepository):
    """Репозиторий для работы с MinIO."""

    @staticmethod
    async def add(data: bytes, object_name: str, ext: str) -> str:
        """
        Загружает объект в MinIO.

        :param data: Байтовые данные изображения.
        :param object_name: Имя объекта в хранилище.
        :param ext: Расширение файла (например, 'jpeg', 'png').
        :return: Имя загруженного объекта.
        :raises HTTPException: Если произошла ошибка при загрузке.
        """
        try:
            minio_client.put_object(
                bucket_name=settings.MINIO_BUCKET_NAME,
                object_name=object_name,
                data=BytesIO(data),
                length=len(data),
                content_type=f"image/{ext}",
            )
            return object_name
        except S3Error as e:
            raise HTTPException(status_code=500, detail=f"Ошибка загрузки в MinIO: {str(e)}")

    @staticmethod
    async def delete(object_name: str) -> None:
        """
        Удаляет объект из MinIO.

        :param object_name: Имя объекта в хранилище.
        :raises HTTPException: Если произошла ошибка при удалении.
        """
        try:
            minio_client.remove_object(settings.MINIO_BUCKET_NAME, object_name)
        except S3Error as e:
            raise HTTPException(status_code=500, detail=f"Ошибка удаления из MinIO: {str(e)}")

    @staticmethod
    async def delete_all() -> None:
        """
        Удаляет все объекты из MinIO.

        :raises HTTPException: Если произошла ошибка при удалении.
        """
        try:
            objects = minio_client.list_objects(settings.MINIO_BUCKET_NAME, recursive=True)
            for obj in objects:
                minio_client.remove_object(settings.MINIO_BUCKET_NAME, obj.object_name)
        except S3Error as e:
            raise HTTPException(
                status_code=500, detail=f"Ошибка удаления всех объектов из MinIO: {str(e)}"
            )

    @staticmethod
    async def create_thumbnail(data: bytes, ext: str) -> bytes:
        """
        Создает миниатюру изображения размером 200x200.

        :param data: Байтовые данные изображения.
        :param ext: Формат изображения ('JPEG', 'PNG' и т. д.).
        :return: Байтовые данные миниатюры.
        """
        with Image.open(BytesIO(data)) as img:
            img.thumbnail((200, 200))
            buf = BytesIO()
            img.save(buf, format=ext.upper())
            return buf.getvalue()
