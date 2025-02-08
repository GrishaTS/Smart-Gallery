
import os
from fastapi import APIRouter, UploadFile, File, HTTPException
from repository import ImageRepository
from schemas import SImage, SImageAdd, SImageId
from utils.add_image import process_image

router = APIRouter(
    prefix='/images',
    tags=['Изображения'],
)

@router.post('/',   
             description='Добавить изображение в базу.',   
             summary='Добавить изображение',   
             response_description='Возвращает ID добавленного изображения')
async def add_image(file: UploadFile = File(...)) -> SImageId:
    allowed_extensions = ['.jpg', '.jpeg', '.png']
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in allowed_extensions:
        raise HTTPException(status_code=400, detail="Ожидается изображение (jpg, png, jpeg)")
    result = await process_image(file)
    image_data = SImageAdd(**result)
    new_image_id = await ImageRepository.add_image(image_data)
    return SImageId(id=new_image_id)



@router.get('/',
            description='Получить список всех изображений в базе.',
            summary='Список изображений',
            response_description='Возвращает список изображений')
async def get_images() -> list[SImage]:
    images = await ImageRepository.get_images()
    return images


@router.get('/{image_id}',
            description='Получить изображение по его ID.',
            summary='Получить изображение',
            response_description='Возвращает данные изображения или сообщение об ошибке')
async def get_image(image_id: int) -> SImage | dict:
    image = await ImageRepository.get_image_by_id(image_id)
    return image if image else {'error': 'Изображение не найдено'}


@router.delete('/{image_id}',
               description='Удалить изображение по его ID.',
               summary='Удалить изображение',
               response_description='Возвращает сообщение об успешном удалении или ошибке')
async def delete_image(image_id: int) -> dict:
    deleted = await ImageRepository.delete_image(image_id)
    return {'message': 'Изображение удалено'} if deleted else {'error': 'Изображение не найдено'}
