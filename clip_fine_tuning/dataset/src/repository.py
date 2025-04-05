from typing import List, Optional

from sqlalchemy import delete, select
from sqlalchemy.exc import IntegrityError

from dataset.src.database import sqlite_client
from dataset.src.models import Clip100Orm


class ClipRepository:
    """Репозиторий для работы с таблицей clip100 в SQLite."""

    @staticmethod
    async def add(image_url: str, descriptions: List[str]) -> bool:
        """
        Добавляет изображение в таблицу.

        :param url: URL изображения.
        :param descriptions: Список текстовых описаний.
        :return: True, если добавление прошло успешно; False при конфликте.
        """
        if len(descriptions) != 10:
            return False
        async with sqlite_client() as session:
            image = Clip100Orm(
                image_url=image_url,
                **{f'description{i+1}': descriptions[i] for i in range(10)},
            )
            session.add(image)
            try:
                await session.commit()
                return True
            except IntegrityError:
                await session.rollback()
                return False

    @staticmethod
    async def get_all() -> List[Clip100Orm]:
        """
        Возвращает все записи из таблицы clip100.

        :return: Список ORM-объектов Clip100Orm.
        """
        async with sqlite_client() as session:
            result = await session.execute(select(Clip100Orm))
            return result.scalars().all()

    @staticmethod
    async def get_by_url(image_url: str) -> Optional[Clip100Orm]:
        async with sqlite_client() as session:
            result = await session.execute(
                select(Clip100Orm).where(Clip100Orm.image_url == image_url)
            )
            return result.scalar_one_or_none()

    @staticmethod
    async def delete_by_url(image_url: str) -> bool:
        async with sqlite_client() as session:
            result = await session.execute(
                delete(Clip100Orm).where(Clip100Orm.image_url == image_url)
            )
            await session.commit()
            return result.rowcount > 0

    @staticmethod
    async def delete_all() -> int:
        async with sqlite_client() as session:
            result = await session.execute(delete(Clip100Orm))
            await session.commit()
            return result.rowcount or 0