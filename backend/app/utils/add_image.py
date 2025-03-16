from pathlib import Path
import uuid
import json
from io import BytesIO
import asyncio
from fastapi import UploadFile, HTTPException
from PIL import Image
from minio import S3Error

from app.config import settings
from app.api import get_image_embedding
from app.database import minio_client, ImageOrm
from app.schemas import SImageAdd

ALLOWED_EXTENSIONS = {'.jpg', '.jpeg', '.png'}

async def upload_to_minio(data: bytes, object_name: str, content_type: str) -> str:
    try:
        minio_client.put_object(
            bucket_name=settings.MINIO_BUCKET_NAME,
            object_name=object_name,
            data=BytesIO(data),
            length=len(data),
            content_type=content_type,
        )
    except S3Error as e:
        raise HTTPException(status_code=500, detail=f'Ошибка загрузки в MinIO: {str(e)}')

async def save_image(img_bytes: bytes, filename: str, ext: str) -> str:
    image_object_name = f'images/{filename}.{ext}'
    await upload_to_minio(img_bytes, image_object_name, f"image/{ext}")
    return image_object_name

async def save_thumbnail(img_bytes: bytes, filename: str, ext: str) -> str:
    def _create_thumbnail(data: bytes) -> bytes:
        with Image.open(BytesIO(data)) as img:
            img.thumbnail((200, 200))
            buf = BytesIO()
            img.save(buf, format=ext)
            return buf.getvalue()

    thumbnail_bytes = await asyncio.to_thread(_create_thumbnail, img_bytes)
    thumbnail_object_name = f'thumbnails/{filename}.{ext}'
    await upload_to_minio(thumbnail_bytes, thumbnail_object_name, f"image/{ext}")
    return thumbnail_object_name

async def save_embedding(image_object_name: str, filename: str, ext='json') -> str:
    image_url = ImageOrm.minio_link(image_object_name)
    embedding = await get_image_embedding(image_url)
    embedding_data = json.dumps(embedding).encode('utf-8')
    embedding_object_name = f'embeddings/{filename}.{ext}'
    await upload_to_minio(embedding_data, embedding_object_name, f"application/{ext}")
    return embedding_object_name

async def add_image_process(file: UploadFile) -> dict:
    if Path(file.filename).suffix.lower() not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail='Разрешены только изображения (jpg, png, jpeg)')
    filename = str(uuid.uuid4())
    img_ext = Path(file.filename).suffix.lower()[1:]
    img_ext = 'JPEG' if img_ext.lower() == 'jpg' else img_ext.upper()

    img_bytes = await file.read()

    image_object_name = await save_image(img_bytes, filename, img_ext)
    thumbnail_object_name = await save_thumbnail(img_bytes, filename, img_ext)
    embedding_object_name = await save_embedding(image_object_name, filename)

    return SImageAdd(
        image_object_name=image_object_name,
        thumbnail_object_name=thumbnail_object_name,
        embedding_object_name=embedding_object_name,
        size=len(img_bytes),
    )
