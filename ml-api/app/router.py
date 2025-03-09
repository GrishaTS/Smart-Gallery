import os
from typing import List
from fastapi import APIRouter, UploadFile, File, HTTPException
from app.schemas import SImage, SImageAdd, SImageId
from app.repository import ImageRepository
from app.utils.add_image import process_image

router_health = APIRouter(prefix="/health", tags=["Изображение"])

@router_health.get("/", tags=['Работоспособность'])
def health_check():
    return {"status": "ok"}

router_image = APIRouter(prefix="/image", tags=["Изображение"])

@router_image.post("/", response_model=SImageId)
async def add_image(file: UploadFile = File(...)):
    allowed_extensions = [".jpg", ".jpeg", ".png"]
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in allowed_extensions:
        raise HTTPException(status_code=400, detail="Ожидается изображение (jpg, png, jpeg)")
    result = await process_image(file)
    image_data = SImageAdd(**result)
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
    deleted = await ImageRepository.delete_image(image_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Изображение не найдено")
    return {"message": "Изображение удалено"}


router_images = APIRouter(prefix="/images", tags=["Изображения"])


@router_images.post("/", response_model=List[SImageId])
async def add_images(files: List[UploadFile] = File(...)):
    allowed_extensions = [".jpg", ".jpeg", ".png"]
    image_ids = []
    for file in files:
        ext = os.path.splitext(file.filename)[1].lower()
        if ext not in allowed_extensions:
            raise HTTPException(status_code=400, detail="Ожидается изображение (jpg, png, jpeg)")
        result = await process_image(file)
        image_data = SImageAdd(**result)
        new_image_id = await ImageRepository.add_image(image_data)
        image_ids.append(SImageId(id=new_image_id))
    return image_ids


@router_images.get("/", response_model=list[SImage])
async def get_images():
    return await ImageRepository.get_images()


@router_images.delete("/")
async def delete_all_images():
    deleted_count = await ImageRepository.delete_all_images()
    return {"message": f"Удалено {deleted_count} изображений"}