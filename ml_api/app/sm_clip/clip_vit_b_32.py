from .base_clip import BaseClip
# import torch
# import open_clip

import numpy as np
from PIL import Image

class ClipVitB32(BaseClip):
    MODEL_NAME = "ViT-B-32"

    def __init__(self):
        pass
        # self.device = "cuda" if torch.cuda.is_available() else "cpu"
        # self.model, self.preprocess, _ = open_clip.create_model_and_transforms(self.MODEL_NAME, pretrained="openai")
        # self.tokenizer = open_clip.get_tokenizer(self.MODEL_NAME)
        # self.model.to(self.device)

    async def get_image_embedding(self, image: Image.Image) -> np.ndarray:
        return np.concatenate([np.zeros(508, dtype=int), np.random.randint(-2, 5, size=4)])
        # image = image.convert("RGB")
        # image = self.preprocess(image).unsqueeze(0).to(self.device)

        # with torch.no_grad():
        #     image_features = self.model.encode_image(image)
        #     image_features /= image_features.norm(dim=-1, keepdim=True)

        # return image_features.cpu().numpy()
    
    async def get_text_embedding(self, text: str) -> np.ndarray:
        return np.concatenate([np.zeros(508, dtype=int), np.random.randint(-2, 5, size=4)])
        # text_tokens = self.tokenizer([text]).to(self.device)

        # with torch.no_grad():
        #     text_features = self.model.encode_text(text_tokens)
        #     text_features /= text_features.norm(dim=-1, keepdim=True)

        # return text_features.cpu().numpy()
