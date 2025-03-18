import json

from minio import Minio

from app.config import settings


# Инициализация Minio-клиента
minio_client = Minio(
    settings.MINIO_ENDPOINT,
    access_key=settings.MINIO_ROOT_USER,
    secret_key=settings.MINIO_ROOT_PASSWORD,
    secure=False,
)


async def create_minio() -> None:
    """Создает бакет в Minio, если он не существует, и задает политику доступа."""
    if not minio_client.bucket_exists(settings.MINIO_BUCKET_NAME):
        minio_client.make_bucket(settings.MINIO_BUCKET_NAME)

    policy = json.dumps({
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Principal": "*",
                "Action": ["s3:GetObject"],
                "Resource": [f"arn:aws:s3:::{settings.MINIO_BUCKET_NAME}/*"],
            }
        ]
    })

    minio_client.set_bucket_policy(settings.MINIO_BUCKET_NAME, policy)


async def delete_minio() -> None:
    """Удаляет все объекты из бакета Minio, затем удаляет сам бакет."""
    if minio_client.bucket_exists(settings.MINIO_BUCKET_NAME):
        objects = minio_client.list_objects(settings.MINIO_BUCKET_NAME, recursive=True)
        for obj in objects:
            minio_client.remove_object(settings.MINIO_BUCKET_NAME, obj.object_name)

        minio_client.remove_bucket(settings.MINIO_BUCKET_NAME)
