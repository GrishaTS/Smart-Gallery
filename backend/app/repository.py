import os
import asyncio
import aiofiles
import json
from sqlalchemy import select, delete
from app.utils import delete_image_process
from app.database import ImageOrm, new_session
from app.schemas import SImageAdd, SImage
from app.api import get_text_embedding, cosine_similarity
from app.config import settings

class ImageRepository:
    @classmethod
    async def add_image(cls, image: SImageAdd) -> int:
        '''Добавляет изображение в базу данных и возвращает его ID.'''
        async with new_session() as session:
            new_image = ImageOrm(**image.model_dump())
            session.add(new_image)
            await session.commit()
            return new_image.id

    @classmethod
    async def get_images(cls) -> list[SImage]:
        '''Возвращает список всех изображений из базы данных.'''
        async with new_session() as session:
            result = await session.execute(select(ImageOrm))
            return [SImage.model_validate(image) for image in result.scalars().all()]

    @classmethod
    async def get_image_by_id(cls, image_id: int) -> SImage | None:
        '''Возвращает изображение по ID или None, если не найдено.'''
        async with new_session() as session:
            image = await session.get(ImageOrm, image_id)
            return SImage.model_validate(image) if image else None

    @classmethod
    async def delete_image(cls, image_id: int) -> bool:
        '''Удаляет изображение по ID из базы данных и файловой системы.'''
        async with new_session() as session:
            image = await session.get(ImageOrm, image_id)
            if not image:
                return False
            await delete_image_process(image)
            await session.delete(image)
            await session.commit()
        return True

    @classmethod
    async def delete_all_images(cls) -> int:
        async with new_session() as session:
            images = await session.execute(select(ImageOrm))
            images = images.scalars().all()
            if not images:
                return 0
            for image in images:
                await delete_image_process(image)
            result = await session.execute(delete(ImageOrm))
            await session.commit()
            return result.rowcount or 0

    @classmethod
    async def search_images(cls, prompt: str):
        text_emb = await get_text_embedding(prompt)
        if not text_emb:
            return []
        
        async with new_session() as session:
            result = await session.execute(select(ImageOrm))
            images = result.scalars().all()
        
        async def read_embedding(image: ImageOrm):
            async with aiofiles.open(image.embedding_object_name, 'r') as f:
                return image, json.loads(await f.read())
        
        embeddings = await asyncio.gather(*[read_embedding(image) for image in images])
        
        filtered_images = [
            SImage.model_validate(image)
            for image, image_emb in embeddings
            if cosine_similarity(text_emb, image_emb) >= settings.CLIP_THRESHOLD
        ]
        return filtered_images
