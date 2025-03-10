from abc import ABC, abstractmethod
import numpy as np
from PIL import Image
from app.config import settings

class BaseClip(ABC):
    MODEL_NAME: str = None

    @abstractmethod
    def get_text_embedding(self, prompt: str) -> np.ndarray:
        ...
    
    @abstractmethod
    def get_image_embedding(self, image: Image.Image) -> np.ndarray:
        ...
    
    @classmethod
    def get_model(cls) -> 'BaseClip':
        for clip_cls in cls.__subclasses__():
            if clip_cls.MODEL_NAME == settings.ML_API_MODEL:
                return clip_cls()
