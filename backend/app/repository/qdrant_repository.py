from qdrant_client.http import models
from app.database.qdrant_client import qdrant_client
from app.config import settings
from app.repository.base_repository import BaseRepository

class QdrantRepository(BaseRepository):
    @staticmethod
    async def add(embedding: list, vector_id: str):
        """Добавляет векторное представление изображения в Qdrant."""
        qdrant_client.upsert(
            collection_name=settings.QDRANT_COLLECTION_NAME,
            points=[
                models.PointStruct(
                    id=vector_id,
                    vector=embedding,
                )
            ]
        )
    
    @staticmethod
    async def get_by_id(vector_id:str):
        result = qdrant_client.retrieve(
            collection_name=settings.QDRANT_COLLECTION_NAME,
            ids=[vector_id],
            with_vectors=True,
        )
        return result[0].vector if result else None

    @staticmethod
    async def delete(vector_id: str):
        """Удаляет изображение из Qdrant."""
        qdrant_client.delete(
            collection_name=settings.QDRANT_COLLECTION_NAME,
            points_selector=models.PointIdsList(points=[vector_id])
        )

    @staticmethod
    async def delete_all():
        """Удаляет все изображения из Qdrant."""
        qdrant_client.delete_collection(settings.QDRANT_COLLECTION_NAME)
        qdrant_client.create_collection(
            collection_name=settings.QDRANT_COLLECTION_NAME,
            vectors_config=models.VectorParams(size=512, distance=models.Distance.COSINE)
        )

    @staticmethod
    async def search(text_embedding: list[float]):
        """Ищет похожие изображения по эмбеддингу в Qdrant с порогом сходства >= 0.3."""
        search_result = qdrant_client.search(
            collection_name=settings.QDRANT_COLLECTION_NAME,
            query_vector=text_embedding,
            score_threshold=settings.CLIP_THRESHOLD,
        )
        return [hit.id for hit in search_result]
