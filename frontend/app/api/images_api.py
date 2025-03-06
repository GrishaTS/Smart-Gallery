import os
import httpx
from functools import wraps
from config import settings
from utils.image_data import ImageData
from .image_api import ImageApi


class ImagesApi:
    def __init__(self, sort_by=None, descending=False):
        self.sort_by = sort_by
        self.descending = descending
        self.images = self.fetch_images()

    @staticmethod
    def fetch_images() -> list[ImageData]:
        with httpx.Client(http1=True) as client:
            response = client.get(f'{settings.API_URL}/images/')
            if response.status_code == 200:
                return [ImageData(**x) for x in response.json()]
        return []

    def update_images(self):
        self.images = self.fetch_images()
        if self.sort_by:
            self.images.sort(key=lambda img: getattr(img, self.sort_by, 0), reverse=self.descending)

    def get_images(self) -> list[ImageData]:
        self.update_images()
        return self.images

    def set_sorting(self, sort_by):
        self.sort_by = sort_by
        self.descending = not self.descending
    
    def get_n_neighbors(self, image_id, n_neighbors) -> list[ImageData]:
        self.update_images()
        image = ImageApi.fetch_image(image_id)
        index = self.images.index(image)
        return self.images[max(0, index - n_neighbors):min(len(self.images), index + n_neighbors + 1)]

    @staticmethod
    def delete_images():
        with httpx.Client(http1=True) as client:
            response = client.delete(f'{settings.API_URL}/images/')
            if response.status_code == 200:
                return response.json()
            return {}


images_api = ImagesApi()
