import json
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy import Integer, DateTime, func
from app.config import settings
from minio import Minio

engine = create_async_engine(settings.POSTGRES_URL)
new_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

minio_client = Minio(
    settings.MINIO_ENDPOINT,
    access_key=settings.MINIO_ROOT_USER,
    secret_key=settings.MINIO_ROOT_PASSWORD,
    secure=False
)

class Model(DeclarativeBase):
    pass


class ImageOrm(Model):
    __tablename__ = 'images'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, index=True)
    image_object_name: Mapped[str]
    thumbnail_object_name: Mapped[str]
    embedding_object_name: Mapped[str]
    uploaded_at: Mapped[str] = mapped_column(DateTime, default=func.now())
    size: Mapped[int]
    
    @staticmethod
    def minio_link(object_name: str):
        return f'{settings.MINIO_BUCKET_URL}/{object_name}'



async def create_db() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.create_all)


async def delete_db() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.drop_all)


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
