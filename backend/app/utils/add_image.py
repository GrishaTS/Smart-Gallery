import os
import uuid
import json
from datetime import datetime
from fastapi import UploadFile
from PIL import Image
from config import settings
import aiofiles
from fastapi.concurrency import run_in_threadpool

async def save_image(file: UploadFile, image_path: str):
    contents = await file.read()
    async with aiofiles.open(image_path, 'wb') as f:
        await f.write(contents)

def _save_thumbnail(image_path: str, thumbnail_path: str, size=(150, 150)):
    with Image.open(image_path) as img:
        img.thumbnail(size)
        img.save(thumbnail_path)

async def save_thumbnail(image_path: str, thumbnail_path: str, size=(150, 150)):
    await run_in_threadpool(_save_thumbnail, image_path, thumbnail_path, size)

async def save_embedding(embedding_path: str):
    embedding = [1, 2, 3]
    async with aiofiles.open(embedding_path, 'w') as f:
        await f.write(json.dumps(embedding))

async def process_image(file: UploadFile) -> tuple[str, str, str, str, int]:
    filename = str(uuid.uuid4())
    ext = os.path.splitext(file.filename)[1]
    
    image_path = os.path.join(settings.IMAGES_PATH, filename + ext)
    await save_image(file, image_path)
    
    thumbnail_path = os.path.join(settings.THUMBNAILS_PATH, filename + ext)
    await save_thumbnail(image_path, thumbnail_path)
    
    embedding_path = os.path.join(settings.EMBEDDINGS_PATH, f'{filename}.json')
    await save_embedding(embedding_path)

    timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
    size = os.path.getsize(image_path)
    
    return dict(image_path=image_path,
                thumbnail_path=thumbnail_path,
                embedding_path=embedding_path,
                timestamp=timestamp,
                size=size)
