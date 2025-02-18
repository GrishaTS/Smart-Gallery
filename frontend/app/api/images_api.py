import httpx
from config import settings
from utils.image_data import ImageData

def fetch_images() -> list[ImageData]:
    with httpx.Client(http1=True) as client:
        response = client.get(f'{settings.API_URL}/images/')
        if response.status_code == 200:
            return list(map(lambda x: ImageData(**x), response.json()))
        return []
