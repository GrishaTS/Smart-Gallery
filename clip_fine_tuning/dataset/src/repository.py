from typing import List, Optional

from sqlalchemy import delete, select
from sqlalchemy.exc import IntegrityError

from dataset.src.database import sqlite_client
from dataset.src.models import Clip100Orm


class ClipRepository:
    """Репозиторий для работы с таблицей clip100 в SQLite."""

    @staticmethod
    def add(image_url: str, descriptions: List[str]) -> bool:
        if len(descriptions) != 10:
            return False
        session = sqlite_client()
        try:
            image = Clip100Orm(
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
    def get_all() -> List[Clip100Orm]:
        session = sqlite_client()
        try:
            result = session.execute(select(Clip100Orm))
            return result.scalars().all()
        finally:
            session.close()

    @staticmethod
    def get_by_url(image_url: str) -> Optional[Clip100Orm]:
        session = sqlite_client()
        try:
            result = session.execute(
                select(Clip100Orm).where(Clip100Orm.image_url == image_url)
            )
            return result.scalar_one_or_none()
        finally:
            session.close()

    @staticmethod
    def delete_by_url(image_url: str) -> bool:
        session = sqlite_client()
        try:
            result = session.execute(
                delete(Clip100Orm).where(Clip100Orm.image_url == image_url)
            )
            session.commit()
            return result.rowcount > 0
        finally:
            session.close()

    @staticmethod
    def delete_all() -> int:
        session = sqlite_client()
        try:
            result = session.execute(delete(Clip100Orm))
            session.commit()
            return result.rowcount or 0
        finally:
            session.close()
