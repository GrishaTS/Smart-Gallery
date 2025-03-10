import io
import os
import httpx
from functools import wraps
from config import settings
from data import ImageData
from .image_api import ImageApi


class ImagesApi:
    def __init__(self, sort_by=None, descending=False):
        self.sort_by = sort_by
        self.descending = descending
        self.images = self.fetch_images()

    @staticmethod
    def fetch_images() -> list[ImageData]:
        with httpx.Client(http1=True) as client:
            response = client.get(f'{settings.BACKEND_URL}/images/')
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
    
    def search_images(self, prompt):
        with httpx.Client(http1=True) as client:
            response = client.get(f'{settings.BACKEND_URL}/images/search/{prompt}')
            if response.status_code == 200:
                return [ImageData(**x) for x in response.json()]
        return []

    def set_sorting(self, sort_by):
        self.sort_by = sort_by
        self.descending = not self.descending
    
    def get_n_neighbors(self, image: ImageData, n_neighbors) -> list[ImageData]:
        self.update_images()
        index = self.images.index(image)
        return self.images[max(0, index - n_neighbors):min(len(self.images), index + n_neighbors + 1)]

    @staticmethod
    def delete_images():
        with httpx.Client(http1=True) as client:
            response = client.delete(f'{settings.BACKEND_URL}/images/')
            if response.status_code == 200:
                return response.json()
            return {}
        
    @staticmethod
    def post_images(file_names: list[str]) -> list:
        files = []
        for file_name in file_names:
            file_path = os.path.join(settings.TEMP_DIR, file_name)
            ext = os.path.splitext(file_name)[1].lower()
            if os.path.exists(file_path):
                with open(file_path, 'rb') as file:
                    files.append(('files', (file_name, io.BytesIO(file.read()), f'image/{ext[1:]}')))
        if files:
            with httpx.Client(http1=True) as client:
                response = client.post(f'{settings.BACKEND_URL}/images/', files=files)
                if response.status_code == 200:
                    for file_name in file_names:
                        file_path = os.path.join(settings.TEMP_DIR, file_name)
                        if os.path.exists(file_path):
                            os.remove(file_path)
                    return response.json()
        
        return []


images_api = ImagesApi()
