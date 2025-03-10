import os
import uuid
import json
from fastapi import UploadFile
from PIL import Image
import aiofiles
import asyncio
from app.config import settings
from app.api import get_image_embedding

async def save_image(file: UploadFile, image_path: str) -> None:
    """Сохраняет загруженное изображение асинхронно."""
    async with aiofiles.open(image_path, 'wb') as f:
        await f.write(await file.read())

def _create_thumbnail(image_path: str, preview_path: str, size: tuple[int, int] = (200, 200)) -> None:
    """Создает и сохраняет уменьшенную версию изображения."""
    with Image.open(image_path) as img:
        img.thumbnail(size)
        img.save(preview_path)

async def save_thumbnail(image_path: str, preview_path: str, size: tuple[int, int] = (200, 200)) -> None:
    """Асинхронно создает миниатюру изображения."""
    await asyncio.to_thread(_create_thumbnail, image_path, preview_path, size)

async def save_embedding(embedding_path: str, image_path: str) -> None:
    """Создает и сохраняет фиктивный эмбеддинг."""
    embedding = await get_image_embedding(image_path)
    async with aiofiles.open(embedding_path, 'w') as f:
        await f.write(json.dumps(embedding))


async def process_image(file: UploadFile) -> dict:
    """Обрабатывает загруженное изображение: сохраняет оригинал, миниатюру и эмбеддинг."""
    filename = f"{uuid.uuid4()}{os.path.splitext(file.filename)[1]}"
    
    image_path = os.path.join(settings.IMAGES_PATH, filename)
    preview_path = os.path.join(settings.THUMBNAILS_PATH, filename)
    embedding_path = os.path.join(settings.EMBEDDINGS_PATH, f"{filename}.json")

    await save_image(file, image_path)
    await asyncio.gather(
        save_thumbnail(image_path, preview_path),
        save_embedding(embedding_path, image_path)
    )

    size = os.path.getsize(image_path)

    return {
        "image_path": image_path,
        "preview_path": preview_path,
        "embedding_path": embedding_path,
        "size": size
    }
