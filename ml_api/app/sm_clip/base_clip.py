from abc import ABC, abstractmethod
from typing import Optional

import numpy as np
from PIL import Image

from app.config import settings


class BaseClip(ABC):
    """
    Абстрактный базовый класс для CLIP-моделей.
    """

    MODEL_NAME: Optional[str] = None

    @abstractmethod
    async def get_text_embedding(self, prompt: str) -> np.ndarray:
        """
        Получает эмбеддинг для текстового запроса.

        :param prompt: Текстовый запрос.
        :return: Векторное представление текста в виде np.ndarray.
        """
        ...

    @abstractmethod
    async def get_image_embedding(self, image: Image.Image) -> np.ndarray:
        """
        Получает эмбеддинг для изображения.

        :param image: Изображение в формате PIL.Image.
        :return: Векторное представление изображения в виде np.ndarray.
        """
        ...

    @classmethod
    def get_model(cls) -> Optional["BaseClip"]:
        """
        Возвращает экземпляр модели CLIP, соответствующей конфигурации.

        :return: Экземпляр класса-наследника BaseClip или None, если модель не найдена.
        """
        for clip_cls in cls.__subclasses__():
            if clip_cls.MODEL_NAME == settings.ML_API_MODEL:
                return clip_cls()
        return None
