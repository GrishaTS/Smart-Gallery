from app.config import settings
import aiofiles
import httpx
import numpy as np

def cosine_similarity(vec1: list, vec2: list) -> float:
    vec1 = np.array(vec1)
    vec2 = np.array(vec2)
    dot_product = np.dot(vec1, vec2)
    norm_vec1 = np.linalg.norm(vec1)
    norm_vec2 = np.linalg.norm(vec2)
    if norm_vec1 == 0 or norm_vec2 == 0:
        return 0.0
    return dot_product / (norm_vec1 * norm_vec2)

async def get_image_embedding(image_url: str):
    print(image_url)
    async with httpx.AsyncClient() as client:
        response: httpx.Response = await client.post(
            f'{settings.ML_API_URL}/embed/image',
            json={'image_url': image_url},
            timeout=10
        )    
    if response.status_code == 200:
        return response.json()
    return []


async def get_text_embedding(prompt: str):
    async with httpx.AsyncClient() as client:
        response: httpx.Response = await client.post(
            f'{settings.ML_API_URL}/embed/text',
            json={'prompt': prompt},
            timeout=10
        )
    if response.status_code == 200:
        return response.json()
    return []
