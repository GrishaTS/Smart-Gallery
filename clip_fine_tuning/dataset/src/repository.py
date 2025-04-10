from typing import List, Optional

from sqlalchemy import delete, select
from sqlalchemy.exc import IntegrityError

from dataset.src.database import sqlite_client
from dataset.src.models import Clip993Orm


class Clip993Repository:
    """
    Репозиторий для взаимодействия с таблицей clip993.

    Методы:
        add: Добавляет новую запись.
        get_all: Возвращает все записи.
        get_by_url: Ищет запись по URL изображения.
        delete_by_url: Удаляет запись по URL.
        delete_all: Удаляет все записи из таблицы.
    """

    @staticmethod
    def add(image_url: str, descriptions: List[str]) -> bool:
        """
        Добавляет новую запись в базу данных.

        Args:
            image_url (str): URL изображения.
            descriptions (List[str]): Список из 10 описаний.

        Returns:
            bool: True, если добавление успешно; False при ошибке или дубликате.
        """
        if len(descriptions) != 10:
            return False
        session = sqlite_client()
        try:
            image = Clip993Orm(
                image_url=image_url,
                **{f'description{i+1}': descriptions[i] for i in range(10)},
            )
            session.add(image)
            session.commit()
            return True
        except IntegrityError:
            session.rollback()
            return False
        finally:
            session.close()

    @staticmethod
    def get_all() -> List[Clip993Orm]:
        """
        Получает все записи из таблицы clip993.

        Returns:
            List[Clip993Orm]: Список ORM-объектов.
        """
        session = sqlite_client()
        try:
            result = session.execute(select(Clip993Orm))
            return result.scalars().all()
        finally:
            session.close()

    @staticmethod
    def get_by_url(image_url: str) -> Optional[Clip993Orm]:
        """
        Получает запись по URL изображения.

        Args:
            image_url (str): URL изображения.

        Returns:
            Optional[Clip993Orm]: Найденный объект или None.
        """
        session = sqlite_client()
        try:
            result = session.execute(
                select(Clip993Orm).where(Clip993Orm.image_url == image_url)
            )
            return result.scalar_one_or_none()
        finally:
            session.close()

    @staticmethod
    def delete_by_url(image_url: str) -> bool:
        """
        Удаляет запись по URL изображения.

        Args:
            image_url (str): URL изображения.

        Returns:
            bool: True, если запись была удалена.
        """
        session = sqlite_client()
        try:
            result = session.execute(
                delete(Clip993Orm).where(Clip993Orm.image_url == image_url)
            )
            session.commit()
            return result.rowcount > 0
        finally:
            session.close()

    @staticmethod
    def delete_all() -> int:
        """
        Удаляет все записи из таблицы clip993.

        Returns:
            int: Количество удалённых записей.
        """
        session = sqlite_client()
        try:
            result = session.execute(delete(Clip993Orm))
            session.commit()
            return result.rowcount or 0
        finally:
            session.close()
