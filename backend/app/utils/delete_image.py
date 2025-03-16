from fastapi import HTTPException
from minio import S3Error
from app.database import ImageOrm

from app.config import settings
from app.database import minio_client


def delete_from_minio(object_name: str):
    """Удаляет объект из MinIO."""
    try:
        minio_client.remove_object(
            settings.MINIO_BUCKET_NAME,
            object_name
        )
    except S3Error as e:
        raise HTTPException(status_code=500, detail=f'Ошибка удаления из MinIO: {str(e)}')

async def delete_image_process(image: ImageOrm):
    delete_from_minio(image.image_object_name)
    delete_from_minio(image.thumbnail_object_name)
    delete_from_minio(image.embedding_object_name)
