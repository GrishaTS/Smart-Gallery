import io
from fastapi import APIRouter, UploadFile, File
from app.sm_clip import model

router_health = APIRouter(prefix="/health", tags=["Проверка"])

@router_health.get("/")
def health_check():
    return {"status": "ok"}


router_embed = APIRouter(prefix="/embed", tags=["Эмбединг"])

@router_embed.post("/image")
async def embed_image(file: UploadFile = File(...)):
    embedding = model.get_image_embedding(io.BytesIO(await file.read()))
    return embedding.tolist()


@router_embed.post("/text/{prompt}")
async def embed_text(prompt: str):
    embedding = model.get_text_embedding(prompt)
    return embedding.tolist()
