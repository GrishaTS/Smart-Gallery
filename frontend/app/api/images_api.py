import io
import os
from typing import List, Optional

import httpx

from app.config import settings
from app.data import ImageData


class ImagesApi:
    """Класс API-клиента для взаимодействия с сервисом изображений."""

    def __init__(self, sort_by: Optional[str] = None, descending: bool = False):
        """
        Инициализирует API-клиент.

        :param sort_by: Поле для сортировки изображений.
        :param descending: Флаг сортировки по убыванию.
        """
        self.sort_by = sort_by
        self.descending = descending
        self.images = self.fetch_images()

    @staticmethod
    def fetch_images() -> List[ImageData]:
        """
        Получает список всех изображений.

        :return: Список объектов ImageData.
        """
        with httpx.Client(http1=True) as client:
            response = client.get(f"{settings.BACKEND_URL}/images/")
            if response.status_code == 200:
                return [ImageData(**x) for x in response.json()]
        return []

    def update_images(self) -> None:
        """
        Обновляет список изображений и сортирует их, если указан параметр сортировки.
        """
        self.images = self.fetch_images()
        if self.sort_by:
            self.images.sort(
                key=lambda img: getattr(img, self.sort_by, 0),
                reverse=self.descending,
            )

    def get_images(self) -> List[ImageData]:
        """
        Получает обновленный список изображений.

        :return: Список объектов ImageData.
        """
        self.update_images()
        return self.images

    def search_images(self, prompt: str) -> List[ImageData]:
        """
        Выполняет поиск изображений по текстовому запросу.

        :param prompt: Поисковый запрос.
        :return: Список найденных изображений.
        """
        with httpx.Client(http1=True) as client:
            response = client.get(f"{settings.BACKEND_URL}/images/search/{prompt}")
            if response.status_code == 200:
                return [ImageData(**x) for x in response.json()]
        return []

    def set_sorting(self, sort_by: str) -> None:
        """
        Устанавливает параметр сортировки изображений.

        :param sort_by: Поле, по которому нужно сортировать.
        """
        self.sort_by = sort_by
        self.descending = not self.descending

    def get_n_neighbors(self, image: ImageData, n_neighbors: int) -> List[ImageData]:
        """
        Возвращает `n_neighbors` ближайших изображений в списке.

        :param image: Изображение, относительно которого выполняется поиск.
        :param n_neighbors: Количество соседей.
        :return: Список ближайших изображений.
        """
        self.update_images()
        index = self.images.index(image)
        return self.images[max(0, index - n_neighbors) : min(len(self.images), index + n_neighbors + 1)]

    @staticmethod
    def delete_images() -> dict:
        """
        Удаляет все изображения.

        :return: Ответ API в формате dict (обычно содержит количество удалённых изображений).
        """
        with httpx.Client(http1=True) as client:
            response = client.delete(f"{settings.BACKEND_URL}/images/")
            if response.status_code == 200:
                return response.json()
        return {}

    @staticmethod
    def post_images(file_names: List[str]) -> List[dict]:
        """
        Загружает несколько изображений на сервер.

        :param file_names: Список имен файлов.
        :return: Ответ API в формате списка словарей (ID загруженных изображений).
        """
        files = []
        for file_name in file_names:
            file_path = os.path.join(settings.TEMP_DIR, file_name)
            ext = os.path.splitext(file_name)[1].lower()
            if os.path.exists(file_path):
                with open(file_path, "rb") as file:
                    files.append(("files", (file_name, io.BytesIO(file.read()), f"image/{ext[1:]}")))

        if files:
            with httpx.Client(http1=True) as client:
                response = client.post(f"{settings.BACKEND_URL}/images/", files=files)
                if response.status_code == 200:
                    # Удаление файлов после успешной загрузки
                    for file_name in file_names:
                        file_path = os.path.join(settings.TEMP_DIR, file_name)
                        if os.path.exists(file_path):
                            os.remove(file_path)
                    return response.json()
        return []


images_api = ImagesApi()
