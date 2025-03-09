from abc import ABC, abstractmethod
import numpy as np
from PIL import Image

class BaseClip(ABC):
    MODEL = None
    IMAGE_PREPROCESSOR = None
    TOKENIZER = None

    @abstractmethod
    def get_text_embedding(prompt: str) -> np.ndarray:
        ...
    
    @abstractmethod
    def get_image_ebedding(image: Image.Image) -> np.ndarray:
        ...
    
    def cosine_similarity(embedding1: np.ndarray, embedding2: np.ndarray) -> float:
        return np.dot(embedding1, embedding2.T).item()
