from .base_clip import BaseClip
import torch
import open_clip

import numpy as np
from PIL import Image

class ClipVitB32(BaseClip):
    MODEL_NAME = "ViT-B-32"
    PRETRAINED = "openai"
    DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

    MODEL, PREPROCESS, _ = open_clip.create_model_and_transforms(MODEL_NAME, pretrained=PRETRAINED)
    TOKENIZER = open_clip.get_tokenizer(MODEL_NAME)
    MODEL.to(DEVICE)

    @classmethod
    def get_image_embedding(cls, image: Image.Image) -> np.ndarray:
        image = image.convert("RGB")
        image = cls.PREPROCESS(image).unsqueeze(0).to(cls.DEVICE)

        with torch.no_grad():
            image_features = cls.MODEL.encode_image(image)
            image_features /= image_features.norm(dim=-1, keepdim=True)

        return image_features.cpu().numpy()
    
    @classmethod
    def get_text_embedding(cls, text: str) -> np.ndarray:
        text_tokens = cls.TOKENIZER([text]).to(cls.DEVICE)

        with torch.no_grad():
            text_features = cls.MODEL.encode_text(text_tokens)
            text_features /= text_features.norm(dim=-1, keepdim=True)

        return text_features.cpu().numpy()
    
