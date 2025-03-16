import asyncio
import io
from fastapi import APIRouter, HTTPException
from app.sm_clip import model
from PIL import Image
import requests
from app.schemas import ImageRequest, TextRequest

router_health = APIRouter(prefix="/health", tags=["Проверка"])

@router_health.get("/")
def health_check():
    return {"status": "ok"}


router_embed = APIRouter(prefix="/embed", tags=["Эмбединг"])

@router_embed.post("/image")
async def embed_image(request: ImageRequest):
    response = requests.get(request.image_url)
    image = None
    if response.status_code == 200:
        image = Image.open(io.BytesIO(response.content))
    if not image:
        raise HTTPException(status_code=400, detail=f"Ошибка загрузки изображения")
    embedding = await asyncio.to_thread(model.get_image_embedding, image)
    return embedding.tolist()


@router_embed.post("/text")
async def embed_text(request: TextRequest):
    embedding = await asyncio.to_thread(model.get_text_embedding, request.text)
    return embedding.tolist()
