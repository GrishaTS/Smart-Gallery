from abc import ABC, abstractmethod
import numpy as np
from PIL import Image
from typing import Optional


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
