from transformers import CLIPProcessor, CLIPModel
import torch
from PIL import Image

clip_model = CLIPModel.from_pretrained("wkcn/TinyCLIP-ViT-61M-32-Text-29M-LAION400M")
clip_processor = CLIPProcessor.from_pretrained("wkcn/TinyCLIP-ViT-61M-32-Text-29M-LAION400M")


def txt_embedding(txt):
    text_inputs = clip_processor(text=[txt], return_tensors="pt", padding=True, truncation=True)
    return clip_model.get_text_features(**text_inputs)

def img_embedding(image_path):
    image = Image.open(image_path).convert("RGB")
    img_input = clip_processor(images=image, return_tensors="pt")
    outputs = clip_model.get_image_features(**img_input)
    return outputs

def is_matching(txt_embed, img_embed):
    return torch.matmul(txt_embed, img_embed.T)
