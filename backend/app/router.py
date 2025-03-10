import os
from typing import List
from fastapi import APIRouter, UploadFile, File, HTTPException
from app.schemas import SImage, SImageAdd, SImageId
from app.repository import ImageRepository
from app.utils.add_image import process_image

router_health = APIRouter(prefix="/health", tags=["Система"])

@router_health.get("/", tags=["Проверка"])
def health_check():
    return {"status": "ok"}

router_image = APIRouter(prefix="/image", tags=["Изображение"])

ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png"}

async def validate_and_process_image(file: UploadFile) -> SImageAdd:
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail="Разрешены только изображения (jpg, png, jpeg)")
    result = await process_image(file)
    return SImageAdd(**result)

@router_image.post("/", response_model=SImageId)
async def add_image(file: UploadFile = File(...)):
    image_data = await validate_and_process_image(file)
    new_image_id = await ImageRepository.add_image(image_data)
    return SImageId(id=new_image_id)

@router_image.get("/{image_id}", response_model=SImage)
async def get_image(image_id: int):
    image = await ImageRepository.get_image_by_id(image_id)
    if not image:
        raise HTTPException(status_code=404, detail="Изображение не найдено")
    return image

@router_image.delete("/{image_id}")
async def delete_image(image_id: int):
    if not await ImageRepository.delete_image(image_id):
        raise HTTPException(status_code=404, detail="Изображение не найдено")
    return {"message": "Изображение удалено"}

router_images = APIRouter(prefix="/images", tags=["Изображения"])

@router_images.post("/", response_model=List[SImageId])
async def add_images(files: List[UploadFile] = File(...)):
    image_ids = [await ImageRepository.add_image(await validate_and_process_image(file)) for file in files]
    return [{"id": image_id} for image_id in image_ids]

@router_images.get("/", response_model=List[SImage])
async def get_images():
    return await ImageRepository.get_images()

@router_images.delete("/")
async def delete_all_images():
    deleted_count = await ImageRepository.delete_all_images()
    return {"message": f"Удалено {deleted_count} изображений"}


@router_images.get("/search/{prompt}")
async def search_images(prompt: str):
    return await ImageRepository.search_images(prompt)
