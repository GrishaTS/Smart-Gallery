import httpx
from functools import wraps
from config import settings
from utils.image_data import ImageData
from .image_api import ImageApi

class ImagesApi(list[ImageData]):
    def __init__(self, sort_by=None, descending=False):
        self.sort_by = sort_by
        self.descending = descending
        super().__init__(self.fetch_images())

    @staticmethod
    def fetch_images() -> list[ImageData]:
        with httpx.Client(http1=True) as client:
            response = client.get(f'{settings.API_URL}/images/')
            if response.status_code == 200:
                return list(map(lambda x: ImageData(**x), response.json()))
            return []

    @staticmethod
    def update_data(func):
        @wraps(func)
        def wrapper(self: 'ImagesApi', *args, **kwargs):
            self.clear()
            self.extend(self.fetch_images())
            if self.sort_by:
                self.sort(key=lambda img_data: getattr(img_data, self.sort_by), reverse=self.descending)
            return func(self, *args, **kwargs)
        return wrapper

    @update_data
    def get_images(self):
        return self
    
    def set_sorting(self, sort_by):
        self.sort_by = sort_by
        self.descending = not self.descending
    
    @update_data
    def get_n_neighbors(self, image_id, n_neighbors):
        image = ImageApi(image_id)
        return self[max(0, self.index(image)-n_neighbors):
                    min(len(self), self.index(image)+n_neighbors+1)]

images_api = ImagesApi()
