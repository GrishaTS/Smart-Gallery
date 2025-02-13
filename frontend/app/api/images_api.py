import httpx
from config import settings
from utils.image_data import ImageData

def fetch_images() -> list[ImageData]:
    with httpx.Client(http1=True) as client:
        print(f'{settings.API_URL}/images/')
        response = client.get(f'{settings.API_URL}/images/')
        if response.status_code == 200:
            print(response.text())
            return list(map(lambda x: ImageData(**x), response.json()))
        print(response.status_code)
        return []
