from typing import List, Optional

from sqlalchemy import delete, select

from app.database import postgres_client
from app.models import ImageOrm
from app.repository.base_repository import BaseRepository
from app.schemas import SImage, SImageAdd


class PostgresRepository(BaseRepository):
    """Репозиторий для работы с базой данных PostgreSQL."""

    @staticmethod
    async def add(image: SImageAdd) -> int:
        """
        Добавляет изображение в базу данных и возвращает его ID.

        :param image: Данные изображения для добавления.
        :return: ID добавленного изображения.
        """
        async with postgres_client() as session:
            new_image = ImageOrm(**image.model_dump())
            session.add(new_image)
            await session.commit()
            return new_image.id

    @staticmethod
    async def get_all() -> List[SImage]:
        """
        Возвращает список всех изображений из базы данных.

        :return: Список объектов SImage.
        """
        async with postgres_client() as session:
            result = await session.execute(select(ImageOrm))
            return [SImage.model_validate(image) for image in result.scalars().all()]

    @staticmethod
    async def get_by_id(image_id: int) -> Optional[SImage]:
        """
        Возвращает изображение по ID или None, если не найдено.

        :param image_id: ID изображения.
        :return: Объект SImage или None.
        """
        async with postgres_client() as session:
            image = await session.get(ImageOrm, image_id)
            return SImage.model_validate(image) if image else None

    @staticmethod
    async def delete(image_id: int) -> bool:
        """
        Удаляет изображение из базы данных.

        :param image_id: ID изображения.
        :return: True, если изображение было удалено, иначе False.
        """
        async with postgres_client() as session:
            image = await session.get(ImageOrm, image_id)
            if not image:
                return False
            await session.delete(image)
            await session.commit()
        return True

    @staticmethod
    async def delete_all() -> int:
        """
        Удаляет все изображения из базы данных.

        :return: Количество удалённых записей.
        """
        async with postgres_client() as session:
            result = await session.execute(delete(ImageOrm))
            await session.commit()
            return result.rowcount or 0

    @staticmethod
    async def search(images_ids: List[int]) -> List[SImage]:
        """
        Ищет изображения по списку ID вектора эмбеддингов.

        :param images_ids: Список ID векторов.
        :return: Список найденных изображений в формате SImage.
        """
        async with postgres_client() as session:
            result = await session.execute(
                select(ImageOrm).where(ImageOrm.embedding_vector_id.in_(images_ids))
            )
            return [SImage.model_validate(image) for image in result.scalars().all()]
