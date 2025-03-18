import io
import requests
from fastapi import APIRouter, HTTPException
from PIL import Image

from app.sm_clip import model
from app.schemas import ImageRequest, TextRequest

# Роутер для проверки состояния сервиса
router_health = APIRouter(prefix="/health", tags=["Проверка"])

@router_health.get("/")
def health_check() -> dict:
    """
    Проверка состояния сервиса.

    :return: Статус сервиса.
    """
    return {"status": "ok"}

# Роутер для получения эмбеддингов
router_embed = APIRouter(prefix="/embed", tags=["Эмбединг"])

@router_embed.post("/image")
async def embed_image(request: ImageRequest) -> list[float]:
    """
    Получает эмбеддинг изображения по URL.

    :param request: Объект запроса с URL изображения.
    :return: Эмбеддинг изображения в формате списка чисел.
    """
    response = requests.get(request.image_url)
    
    if response.status_code == 200:
        image = Image.open(io.BytesIO(response.content))
    else:
        raise HTTPException(status_code=400, detail="Ошибка загрузки изображения")
    
    embedding = await model.get_image_embedding(image)
    return embedding.tolist()

@router_embed.post("/text")
async def embed_text(request: TextRequest) -> list[float]:
    """
    Получает эмбеддинг текста.

    :param request: Объект запроса с текстом.
    :return: Эмбеддинг текста в формате списка чисел.
    """
    embedding = await model.get_text_embedding(request.text)
    return embedding.tolist()
