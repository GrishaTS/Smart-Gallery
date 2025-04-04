import uuid
from pathlib import Path
from typing import List

from fastapi import HTTPException, UploadFile

from app.api import get_image_embedding, get_text_embedding
from app.models import ImageOrm
from app.repository.base_repository import BaseRepository
from app.repository.minio_repository import MinioRepository
from app.repository.postgres_repository import PostgresRepository
from app.repository.qdrant_repository import QdrantRepository
from app.schemas import SImage, SImageAdd


class Repository(BaseRepository):
    """Фасадный репозиторий для управления изображениями."""

    ALLOWED_EXTENSIONS = {"JPG", "JPEG", "PNG"}

    @staticmethod
    async def add(file: UploadFile) -> int:
        """
        Загружает изображение, создаёт миниатюру, сохраняет эмбеддинг и метаданные.

        :param file: Загружаемый файл.
        :return: ID сохранённого изображения.
        :raises HTTPException: Если расширение файла недопустимо.
        """
        db_id = str(uuid.uuid4())
        img_ext = Path(file.filename).suffix.upper()[1:]
        if img_ext not in Repository.ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=400, detail="Разрешены только изображения (jpg, png, jpeg)"
            )

        img_ext = "JPEG" if img_ext == "JPG" else img_ext

        img_bytes = await file.read()
        image_object_name = f"images/{db_id}.{img_ext}"
        await MinioRepository.add(img_bytes, image_object_name, img_ext)

        thumbnail_bytes = await MinioRepository.create_thumbnail(img_bytes, img_ext)
        thumbnail_object_name = f"thumbnail/{db_id}.{img_ext}"
        await MinioRepository.add(thumbnail_bytes, thumbnail_object_name, img_ext)

        embedding = await get_image_embedding(ImageOrm.minio_link(image_object_name))
        embedding_vector_id = db_id
        await QdrantRepository.add(embedding, embedding_vector_id)

        return await PostgresRepository.add(
            SImageAdd(
                image_object_name=image_object_name,
                thumbnail_object_name=thumbnail_object_name,
                embedding_vector_id=embedding_vector_id,
                size=len(img_bytes),
            )
        )

    @staticmethod
    async def get_by_id(image_id: int) -> SImage:
        """
        Получает изображение по ID.

        :param image_id: ID изображения.
        :return: Объект SImage.
        """
        return await PostgresRepository.get_by_id(image_id)

    @staticmethod
    async def get_all() -> List[SImage]:
        """
        Получает список всех изображений.

        :return: Список объектов SImage.
        """
        return await PostgresRepository.get_all()

    @staticmethod
    async def delete(image_id: int) -> bool:
        """
        Удаляет изображение по ID из всех хранилищ.

        :param image_id: ID изображения.
        :return: True, если изображение удалено, иначе False.
        """
        image: SImage = await PostgresRepository.get_by_id(image_id)
        if not image:
            return False

        await MinioRepository.delete(image.image_object_name)
        await MinioRepository.delete(image.thumbnail_object_name)
        await QdrantRepository.delete(image.embedding_vector_id)
        await PostgresRepository.delete(image.id)
        return True

    @staticmethod
    async def delete_all() -> int:
        """
        Удаляет все изображения из MinIO, Qdrant и PostgreSQL.

        :return: Количество удалённых записей.
        """
        await MinioRepository.delete_all()
        await QdrantRepository.delete_all()
        return await PostgresRepository.delete_all()

    @staticmethod
    async def search(prompt: str) -> List[SImage]:
        """
        Ищет изображения по текстовому запросу.

        :param prompt: Текстовый запрос.
        :return: Список найденных изображений.
        """
        text_embedding = await get_text_embedding(prompt)
        images_ids = await QdrantRepository.search(text_embedding)
        return await PostgresRepository.search(images_ids)
