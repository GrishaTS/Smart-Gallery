import base64
import re
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from config import settings


@dataclass
class ImageData:
    """
    Класс для представления данных об изображении.

    :param id: Уникальный идентификатор изображения.
    :param image_object_name: Имя объекта изображения в MinIO.
    :param thumbnail_object_name: Имя миниатюры изображения в MinIO.
    :param embedding_vector_id: Идентификатор вектора эмбеддинга.
    :param uploaded_at: Дата и время загрузки.
    :param size: Размер файла в байтах.
    """

    id: Optional[int] = None
    image_object_name: Optional[str] = None
    thumbnail_object_name: Optional[str] = None
    embedding_vector_id: Optional[str] = None
    uploaded_at: Optional[datetime] = None
    size: Optional[int] = None

    def __post_init__(self) -> None:
        """
        Обрабатывает строковое значение `uploaded_at`, преобразуя его в `datetime`.
        Если формат времени не совпадает с ожидаемым, устанавливает `None`.
        """
        if isinstance(self.uploaded_at, str) and re.fullmatch(
            r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{6}", self.uploaded_at
        ):
            self.uploaded_at = datetime.strptime(self.uploaded_at, "%Y-%m-%dT%H:%M:%S.%f")
        else:
            self.uploaded_at = None

    def __eq__(self, other: object) -> bool:
        """
        Сравнивает два объекта `ImageData` по их `id`.

        :param other: Другой объект для сравнения.
        :return: True, если `id` совпадают и не являются `None`, иначе False.
        """
        return isinstance(other, ImageData) and self.id is not None and self.id == other.id

    @staticmethod
    def minio_link(object_name: str) -> str:
        """
        Генерирует полный URL для объекта MinIO.

        :param object_name: Имя объекта в MinIO.
        :return: Полный URL объекта.
        """
        return f"{settings.MINIO_BUCKET_URL}/{object_name}"
