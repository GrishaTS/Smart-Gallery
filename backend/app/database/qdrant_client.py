from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams

from app.config import settings


# Инициализация клиента Qdrant
qdrant_client = QdrantClient(
    host=settings.QDRANT_HOST,
    port=settings.QDRANT_PORT,
)


async def create_qdrant() -> None:
    """Создает коллекцию в Qdrant, если она не существует."""
    if not qdrant_client.collection_exists(settings.QDRANT_COLLECTION_NAME):
        qdrant_client.create_collection(
            collection_name=settings.QDRANT_COLLECTION_NAME,
            vectors_config=VectorParams(size=512, distance=Distance.COSINE),
        )


async def delete_qdrant() -> None:
    """Удаляет коллекцию из Qdrant."""
    qdrant_client.delete_collection(collection_name=settings.QDRANT_COLLECTION_NAME)
