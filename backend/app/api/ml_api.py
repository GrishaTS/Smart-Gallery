import httpx

from app.config import settings


async def get_image_embedding(image_url: str) -> list[int]:
    """Получает эмбеддинг изображения через ML API."""
    async with httpx.AsyncClient() as client:
        response: httpx.Response = await client.post(
            f"{settings.ML_API_URL}/embed/image",
            json={"image_url": image_url},
            timeout=10,
        )

    if response.status_code == 200:
        return response.json()
    
    return []


async def get_text_embedding(prompt: str) -> list[int]:
    """Получает эмбеддинг текста через ML API."""
    async with httpx.AsyncClient() as client:
        response: httpx.Response = await client.post(
            f"{settings.ML_API_URL}/embed/text",
            json={"text": prompt},
            timeout=10,
        )

    if response.status_code == 200:
        return response.json()
    
    return []
