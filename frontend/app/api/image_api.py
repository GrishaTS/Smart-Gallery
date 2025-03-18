import io
import os

import httpx

from app.config import settings
from app.data import ImageData


class ImageApi:
    """Класс API-клиента для взаимодействия с сервисом изображений."""

    @staticmethod
    def fetch_image(image_id: int) -> ImageData:
        """
        Получает данные изображения по ID.

        :param image_id: Уникальный идентификатор изображения.
        :return: Объект ImageData с данными изображения или пустой объект, если изображение не найдено.
        """
        with httpx.Client(http1=True) as client:
            response = client.get(f"{settings.BACKEND_URL}/image/{image_id}")
            if response.status_code == 200:
                return ImageData(**response.json())
        return ImageData()

    @staticmethod
    def delete_image(image_id: int) -> dict:
        """
        Удаляет изображение по ID.

        :param image_id: Уникальный идентификатор изображения.
        :return: Ответ API в формате dict (обычно содержит сообщение об удалении).
        """
        with httpx.Client(http1=True) as client:
            response = client.delete(f"{settings.BACKEND_URL}/image/{image_id}")
            if response.status_code == 200:
                return response.json()
        return {}

    @staticmethod
    def post_image(file_name: str) -> dict:
        """
        Загружает изображение на сервер.

        :param file_name: Имя файла изображения.
        :return: Ответ API в формате dict (обычно содержит ID загруженного изображения).
        """
        file_path = os.path.join(settings.TEMP_DIR, file_name)
        ext = os.path.splitext(file_name)[1].lower()

        if os.path.exists(file_path):
            with open(file_path, "rb") as file:
                files = {
                    "file": (file_name, io.BytesIO(file.read()), f"image/{ext[1:]}")
                }
                with httpx.Client(http1=True) as client:
                    response = client.post(f"{settings.BACKEND_URL}/image/", files=files)
                    if response.status_code == 200:
                        os.remove(file_path)
                        return response.json()
        return {}
