import os
import uuid
import json
from fastapi import UploadFile
from PIL import Image
import aiofiles
from fastapi.concurrency import run_in_threadpool
from app.config import settings

async def save_image(file: UploadFile, image_path: str):
    contents = await file.read()
    async with aiofiles.open(image_path, 'wb') as f:
        await f.write(contents)

def _save_thumbnail(image_path: str, preview_path: str, size=(150, 150)):
    with Image.open(image_path) as img:
        img.thumbnail(size)
        img.save(preview_path)

async def save_thumbnail(image_path: str, preview_path: str, size=(200, 200)):
    await run_in_threadpool(_save_thumbnail, image_path, preview_path, size)

async def save_embedding(embedding_path: str):
    embedding = [1, 2, 3]
    async with aiofiles.open(embedding_path, 'w') as f:
        await f.write(json.dumps(embedding))

async def process_image(file: UploadFile) -> dict:
    filename = str(uuid.uuid4())
    ext = os.path.splitext(file.filename)[1]

    image_path = os.path.join(settings.IMAGES_PATH, filename + ext)
    preview_path = os.path.join(settings.THUMBNAILS_PATH, filename + ext)
    embedding_path = os.path.join(settings.EMBEDDINGS_PATH, f'{filename}.json')

    await save_image(file, image_path)
    await save_thumbnail(image_path, preview_path)
    await save_embedding(embedding_path)

    size = os.path.getsize(image_path)

    image_url = os.path.join(settings.IMAGES_PATH, filename + ext)
    preview_url = os.path.join(settings.THUMBNAILS_PATH, filename + ext)
    embedding_url = os.path.join(settings.EMBEDDINGS_PATH, f'{filename}.json')

    return {
        "image_path": image_url,
        "preview_path": preview_url,
        "embedding_path": embedding_url,
        "size": size
    }
