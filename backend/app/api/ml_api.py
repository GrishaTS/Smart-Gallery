from app.config import settings
import aiofiles
import httpx
import numpy as np

def cosine_similarity(vec1: list, vec2: list) -> float:
    """Вычисляет косинусное сходство между двумя векторами."""
    vec1 = np.array(vec1)
    vec2 = np.array(vec2)
    dot_product = np.dot(vec1, vec2)
    norm_vec1 = np.linalg.norm(vec1)
    norm_vec2 = np.linalg.norm(vec2)
    if norm_vec1 == 0 or norm_vec2 == 0:
        return 0.0
    return dot_product / (norm_vec1 * norm_vec2)

async def get_image_embedding(image_path: str):
    async with aiofiles.open(image_path, "rb") as f:
        image_bytes = await f.read()
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{settings.ML_API_URL}/embed/image",
            files={"file": ("image.png", image_bytes, "image/png")}
        )    
    if response.status_code == 200:
        return response.json()
    return []

async def get_image_embedding(image_path: str):
    async with aiofiles.open(image_path, "rb") as f:
        image_bytes = await f.read()
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{settings.ML_API_URL}/embed/image",
            files={"file": ("image.png", image_bytes, "image/png")}
        )    
    if response.status_code == 200:
        return response.json()
    return []


async def get_text_embedding(prompt: str):
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{settings.ML_API_URL}/embed/text/{prompt}")
    if response.status_code == 200:
        return response.json()
    return []
