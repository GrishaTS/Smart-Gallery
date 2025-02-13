import flet as ft
from api import images_api
from .base_view import BaseView

class ImagesView(BaseView):
    def __init__(self, page: ft.Page):
        super().__init__('/', page)

        self.assemble_page()
    
    def assemble_page(self):
        self.controls = [self.get_image_grid()]
    
    def get_image_grid(self):
        grid = ft.GridView(runs_count=3, max_extent=140, spacing=10, expand=True)
        print(images_api.fetch_images())
        # for i in images_api.fetch_images():
            # grid.controls.append(
            #     ft.Container(
            #         content=ft.Image(src=preview_img, expand=True, fit='cover'),
            #         on_click=lambda _, img=img_id: page.go(f'/image', img=img, sort=sort_order, order=order_direction),
            #         tooltip=f'{date_create}\n{size} байт',
            #     )
            # )

        return grid