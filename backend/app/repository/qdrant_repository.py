import asyncio
from typing import List, Optional

from qdrant_client.http import models

from app.config import settings
from app.database.qdrant_client import qdrant_client
from app.repository.base_repository import BaseRepository


class QdrantRepository(BaseRepository):
    """Репозиторий для работы с Qdrant."""

    @staticmethod
    async def add(embedding: List[float], vector_id: str) -> None:
        """
        Добавляет векторное представление изображения в Qdrant.

        :param embedding: Векторное представление изображения.
        :param vector_id: Уникальный идентификатор вектора.
        """
        await asyncio.to_thread(
            qdrant_client.upsert,
            collection_name=settings.QDRANT_COLLECTION_NAME,
            points=[models.PointStruct(id=vector_id, vector=embedding)],
        )

    @staticmethod
    async def get_by_id(vector_id: str) -> Optional[List[float]]:
        """
        Получает вектор по ID.

        :param vector_id: Уникальный идентификатор вектора.
        :return: Вектор изображения или None, если не найден.
        """
        result = await asyncio.to_thread(
            qdrant_client.retrieve,
            collection_name=settings.QDRANT_COLLECTION_NAME,
            ids=[vector_id],
            with_vectors=True,
        )
        return result[0].vector if result else None

    @staticmethod
    async def delete(vector_id: str) -> None:
        """
        Удаляет изображение из Qdrant.

        :param vector_id: Уникальный идентификатор вектора.
        """
        await asyncio.to_thread(
            qdrant_client.delete,
            collection_name=settings.QDRANT_COLLECTION_NAME,
            points_selector=models.PointIdsList(points=[vector_id]),
        )

    @staticmethod
    async def delete_all() -> None:
        """
        Удаляет все изображения из Qdrant и пересоздаёт коллекцию.
        """
        await asyncio.to_thread(qdrant_client.delete_collection, settings.QDRANT_COLLECTION_NAME)
        await asyncio.to_thread(
            qdrant_client.create_collection,
            collection_name=settings.QDRANT_COLLECTION_NAME,
            vectors_config=models.VectorParams(size=512, distance=models.Distance.COSINE),
        )

    @staticmethod
    async def search(embedding: List[float]) -> List[str]:
        """
        Ищет похожие изображения по эмбеддингу в Qdrant.

        :param embedding: Векторное представление запроса.
        :return: Список идентификаторов найденных векторов.
        """
        search_result = await asyncio.to_thread(
            qdrant_client.search,
            collection_name=settings.QDRANT_COLLECTION_NAME,
            query_vector=embedding,
            score_threshold=settings.CLIP_THRESHOLD,
        )
        return [hit.id for hit in search_result]
