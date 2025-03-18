from datetime import datetime

from pydantic import BaseModel, ConfigDict


class SImageAdd(BaseModel):
    """
    Схема для добавления изображения.

    :param image_object_name: Имя объекта изображения в MinIO.
    :param thumbnail_object_name: Имя миниатюры изображения в MinIO.
    :param embedding_vector_id: Идентификатор вектора эмбеддинга.
    :param size: Размер файла в байтах.
    :param uploaded_at: Дата загрузки (может быть None).
    """
    image_object_name: str
    thumbnail_object_name: str
    embedding_vector_id: str
    size: int
    uploaded_at: datetime | None = None


class SImage(SImageAdd):
    """
    Расширенная схема изображения с ID.

    :param id: Уникальный идентификатор изображения в базе данных.
    """
    id: int
    model_config = ConfigDict(from_attributes=True)


class SImageId(BaseModel):
    """
    Схема для передачи ID изображения.

    :param id: Уникальный идентификатор изображения.
    """
    id: int
