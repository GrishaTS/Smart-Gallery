from typing import List
from fastapi import APIRouter, UploadFile, File, HTTPException
from app.schemas import SImage, SImageId
from app.repository import Repository

router_health = APIRouter(prefix="/health", tags=["Система"])

@router_health.get("/", tags=["Проверка"])
def health_check():
    return {"status": "ok"}

router_image = APIRouter(prefix="/image", tags=["Изображение"])

@router_image.post("/", response_model=SImageId)
async def add_image(file: UploadFile = File(...)):
    new_image_id = await Repository.add(file)
    return SImageId(id=new_image_id)

@router_image.get("/{image_id}", response_model=SImage)
async def get_image(image_id: int):
    image = await Repository.get_by_id(image_id)
    if not image:
        raise HTTPException(status_code=404, detail="Изображение не найдено")
    return image

@router_image.delete("/{image_id}")
async def delete_image(image_id: int):
    if not await Repository.delete(image_id):
        raise HTTPException(status_code=404, detail="Изображение не найдено")
    return {"message": "Изображение удалено"}

router_images = APIRouter(prefix="/images", tags=["Изображения"])

@router_images.post("/", response_model=List[SImageId])
async def add_images(files: List[UploadFile] = File(...)):
    image_ids = [await Repository.add(file) for file in files]
    return [SImageId(id=image_id) for image_id in image_ids]

@router_images.get("/", response_model=List[SImage])
async def get_images():
    return await Repository.get_all()

@router_images.delete("/")
async def delete_all_images():
    deleted_count = await Repository.delete_all()
    return {"message": f"Удалено {deleted_count} изображений"}


@router_images.get("/search/{prompt}")
async def search_images(prompt: str):
    return await Repository.search(prompt)
