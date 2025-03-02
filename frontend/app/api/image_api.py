import io
import os
import httpx
from functools import wraps
from config import settings
from utils.image_data import ImageData

class ImageApi(ImageData):
    def __init__(self, image_id, sort_by=None, descending=False):
        super().__init__(**self.fetch_image(image_id))

    @staticmethod
    def fetch_image(image_id) -> ImageData:
        with httpx.Client(http1=True) as client:
            response = client.get(f'{settings.API_URL}/image/{image_id}')
            if response.status_code == 200:
                return response.json()
        return {}

    @staticmethod
    def delete_image(image_id: int) -> dict:
        with httpx.Client(http1=True) as client:
            response = client.delete(f'{settings.API_URL}/image/{image_id}')
            if response.status_code == 200:
                return response.json()
        return {}
    
    @staticmethod
    def post_image(file_name: str):
        file_path = os.path.join(settings.TEMP_DIR, file_name)
        ext = os.path.splitext(file_name)[1].lower()
        files = {'file': (file_name, io.BytesIO(open(file_path, 'rb').read()), f'image/{ext[1:]}')}
        os.remove(file_path)
        with httpx.Client(http1=True) as client:
            response = client.post(f'{settings.API_URL}/image/', files=files)
            if response.status_code == 200:
                return response.json()
        return []
        

    @staticmethod
    def update_data(func):
        @wraps(func)
        def wrapper(self: 'ImageApi', *args, **kwargs):
            super().__init__(**self.fetch_image(self.id))
            return func(self, *args, **kwargs)
        return wrapper

    @update_data
    def get_image(self):
        return self
