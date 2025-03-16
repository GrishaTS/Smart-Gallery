from app.config import settings
import httpx
import numpy as np

async def get_image_embedding(image_url: str):
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
            json={'text': prompt},
            timeout=10
        )
    if response.status_code == 200:
        return response.json()
    return []
