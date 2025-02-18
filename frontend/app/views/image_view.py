import flet as ft
from config import settings
from utils.image_data import ImageData
import httpx

class ImageView(ft.View):
    ...
    # def __init__(self, page: ft.Page):
    #     super().__init__(route="/")
    #     self.page = page
    #     self.images = ft.Column()
    #     self.load_images()
    #     self.controls = [self.images]

    # def load_images(self):
    #     try:
    #         response = httpx.get(f"{settings.API_URL}/images/")
    #         if response.status_code == 200:
    #             images_data = response.json()
    #             self.images.controls = [
    #                 ft.Image(src=img["image_path"]) for img in images_data
    #             ]
    #             self.page.update()
    #     except Exception as e:
    #         print(f"Error loading images: {e}")