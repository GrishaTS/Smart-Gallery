from pydantic import BaseModel


class ImageRequest(BaseModel):
    """
    Модель запроса для получения эмбеддинга изображения.
    """

    image_url: str


class TextRequest(BaseModel):
    """
    Модель запроса для получения эмбеддинга текста.
    """

    text: str
