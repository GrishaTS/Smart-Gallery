from sqlalchemy import select, delete
from app.database import postgres_client
from app.models import ImageOrm
from app.schemas import SImageAdd, SImage
from app.repository.base_repository import BaseRepository

class PostgresRepository(BaseRepository):
    @staticmethod
    async def add(image: SImageAdd) -> int:
        """Добавляет изображение в базу данных и возвращает его ID."""
        async with postgres_client() as session:
            new_image = ImageOrm(**image.model_dump())
            session.add(new_image)
            await session.commit()
            return new_image.id

    @staticmethod
    async def get_all() -> list[SImage]:
        """Возвращает список всех изображений из базы данных."""
        async with postgres_client() as session:
            result = await session.execute(select(ImageOrm))
            return [SImage.model_validate(image) for image in result.scalars().all()]

    @staticmethod
    async def get_by_id(image_id: int) -> SImage | None:
        '''Возвращает изображение по ID или None, если не найдено.'''
        async with postgres_client() as session:
            image = await session.get(ImageOrm, image_id)
            return SImage.model_validate(image) if image else None
        
    @staticmethod
    async def delete(image_id: int) -> bool:
        """Удаляет изображение из PostgreSQL и MinIO."""
        async with postgres_client() as session:
            image = await session.get(ImageOrm, image_id)
            if not image:
                return False
            await session.delete(image)
            await session.commit()
        return True

    @staticmethod
    async def delete_all() -> int:
        """Удаляет все изображения из PostgreSQL и MinIO."""
        async with postgres_client() as session:
            result = await session.execute(delete(ImageOrm))
            await session.commit()
            return result.rowcount or 0

    @staticmethod
    async def search(images_ids) -> list[SImage]:
        async with postgres_client() as session:
            result = await session.execute(
                select(ImageOrm).where(ImageOrm.embedding_vector_id.in_(images_ids))
            )
            return [SImage.model_validate(image) for image in result.scalars().all()]