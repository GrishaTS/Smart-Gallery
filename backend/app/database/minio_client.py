import json
from app.config import settings
from minio import Minio

minio_client = Minio(
    settings.MINIO_ENDPOINT,
    access_key=settings.MINIO_ROOT_USER,
    secret_key=settings.MINIO_ROOT_PASSWORD,
    secure=False
)


async def create_minio() -> None:
    if not minio_client.bucket_exists(settings.MINIO_BUCKET_NAME):
        minio_client.make_bucket(settings.MINIO_BUCKET_NAME)

    minio_client.set_bucket_policy(
        settings.MINIO_BUCKET_NAME, 
        policy=json.dumps({
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Principal": "*",
                    "Action": ["s3:GetObject"],
                    "Resource": [f"arn:aws:s3:::{settings.MINIO_BUCKET_NAME}/*"]
                }
            ]
        })
    )

async def delete_minio() -> None:
    if minio_client.bucket_exists(settings.MINIO_BUCKET_NAME):
        minio_client.remove_bucket(settings.MINIO_BUCKET_NAME)
