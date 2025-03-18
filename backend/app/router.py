import asyncio
from typing import List

from fastapi import APIRouter, File, HTTPException, UploadFile

from app.repository import Repository
from app.schemas import SImage, SImageId

# Роутер для проверки состояния системы
router_health = APIRouter(prefix="/health", tags=["Система"])


@router_health.get("/", tags=["Проверка"])
def health_check() -> dict:
    """Проверка состояния API."""
    return {"status": "ok"}


# Роутер для операций с одним изображением
router_image = APIRouter(prefix="/image", tags=["Изображение"])


@router_image.post("/", response_model=SImageId)
async def add_image(file: UploadFile = File(...)) -> SImageId:
    """
    Загружает одно изображение в систему.

    :param file: Загружаемый файл.
    :return: ID загруженного изображения.
    """
    new_image_id = await Repository.add(file)
    return SImageId(id=new_image_id)


@router_image.get("/{image_id}", response_model=SImage)
async def get_image(image_id: int) -> SImage:
    """
    Получает информацию об изображении по его ID.

    :param image_id: ID изображения.
    :return: Объект SImage.
    :raises HTTPException: Если изображение не найдено.
    """
    image = await Repository.get_by_id(image_id)
    if not image:
        raise HTTPException(status_code=404, detail="Изображение не найдено")
    return image


@router_image.delete("/{image_id}")
async def delete_image(image_id: int) -> dict:
    """
    Удаляет изображение по ID.

    :param image_id: ID изображения.
    :return: Сообщение о статусе операции.
    :raises HTTPException: Если изображение не найдено.
    """
    if not await Repository.delete(image_id):
        raise HTTPException(status_code=404, detail="Изображение не найдено")
    return {"message": "Изображение удалено"}


# Роутер для работы с несколькими изображениями
router_images = APIRouter(prefix="/images", tags=["Изображения"])


@router_images.post("/", response_model=List[SImageId])
async def add_images(files: List[UploadFile] = File(...)) -> List[SImageId]:
    """
    Загружает несколько изображений в систему.

    :param files: Список загружаемых файлов.
    :return: Список ID загруженных изображений.
    """
    image_ids = await asyncio.gather(*(Repository.add(file) for file in files))
    return [SImageId(id=image_id) for image_id in image_ids]


@router_images.get("/", response_model=List[SImage])
async def get_images() -> List[SImage]:
    """
    Получает список всех изображений.

    :return: Список объектов SImage.
    """
    return await Repository.get_all()


@router_images.delete("/")
async def delete_all_images() -> dict:
    """
    Удаляет все изображения из системы.

    :return: Сообщение с количеством удалённых изображений.
    """
    deleted_count = await Repository.delete_all()
    return {"message": f"Удалено {deleted_count} изображений"}


@router_images.get("/search/{prompt}")
async def search_images(prompt: str) -> List[SImage]:
    """
    Ищет изображения по текстовому запросу.

    :param prompt: Текстовый запрос.
    :return: Список найденных изображений.
    """
    return await Repository.search(prompt)
