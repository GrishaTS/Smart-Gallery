import flet as ft
from api import images_api
from .base_view import BaseView

class ImagesView(BaseView):
    def __init__(self, page: ft.Page):
        super().__init__('/', page)
        self.page = page
        self.assemble_page()
    
    def assemble_page(self):
        self.controls = [ft.Text(str(images_api.fetch_images())),
                         self.get_image_grid(),]
    
    def get_image_grid(self):
        grid = ft.GridView(runs_count=3, max_extent=140, spacing=10, expand=True)
        for img in images_api.fetch_images():
            grid.controls.append(
                ft.Container(
                    content=ft.Image(src=img.preview_path, expand=True, fit='cover'),
                    on_click=lambda _, img_id=img.id: self.page.go('/image', img=img_id), # add sort
                    tooltip=f'{img.uploaded_at}\n{img.size} байт',
                )
            )
        
        return grid