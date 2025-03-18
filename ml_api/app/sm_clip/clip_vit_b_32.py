import torch
import open_clip
import numpy as np
from PIL import Image

from .base_clip import BaseClip


class ClipVitB32(BaseClip):
    """
    Реализация CLIP-модели ViT-B-32 для получения эмбеддингов изображений и текстов.
    """

    MODEL_NAME = "ViT-B-32"

    def __init__(self):
        """
        Инициализирует модель CLIP ViT-B-32.
        """
        self.device: str = "cuda" if torch.cuda.is_available() else "cpu"
        self.model, self.preprocess, _ = open_clip.create_model_and_transforms(
            self.MODEL_NAME, pretrained="openai"
        )
        self.tokenizer = open_clip.get_tokenizer(self.MODEL_NAME)
        self.model.to(self.device)

    async def get_image_embedding(self, image: Image.Image) -> np.ndarray:
        """
        Получает эмбеддинг изображения.

        :param image: Изображение в формате PIL.Image.
        :return: Векторное представление изображения в виде np.ndarray.
        """
        image = image.convert("RGB")
        image = self.preprocess(image).unsqueeze(0).to(self.device)

        with torch.no_grad():
            image_features = self.model.encode_image(image)
            image_features /= image_features.norm(dim=-1, keepdim=True)

        return image_features.cpu().numpy()[0]

    async def get_text_embedding(self, text: str) -> np.ndarray:
        """
        Получает эмбеддинг текста.

        :param text: Входной текст.
        :return: Векторное представление текста в виде np.ndarray.
        """
        text_tokens = self.tokenizer([text]).to(self.device)

        with torch.no_grad():
            text_features = self.model.encode_text(text_tokens)
            text_features /= text_features.norm(dim=-1, keepdim=True)

        return text_features.cpu().numpy()[0]
