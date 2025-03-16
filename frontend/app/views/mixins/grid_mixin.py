import flet as ft
from abc import ABC, abstractmethod
from data import ImageData

class GridMixin(ABC):
    GRID_SELECTION_MODE = False

    def __init__(self):
        self.grid = ft.GridView(runs_count=3, max_extent=140, spacing=10, expand=True)
        self.selected_images_id = []
        super().__init__()
        self.page: ft.Page
    
    abstractmethod
    def get_images() -> list[ImageData]:
        ...

    def load_grid(self, update=True):
        if update:
            self.grid.clean()
        images: list[ImageData] = self.get_images()
        if self.GRID_SELECTION_MODE:
            if not hasattr(self, 'add_selection_image'):
                raise AttributeError('add_selection_image не инициализирована')
            for img in images:
                self.grid.controls.append(ft.Container(
                    content=ft.Image(src=ImageData.minio_link(img.thumbnail_object_name), expand=True, fit='cover'),
                    on_click=lambda _, image_id=img.id: self.add_selection_image(image_id),
                    tooltip=f'{img.uploaded_at}\n{img.size} байт',
                    border=ft.border.all(3, 'blue') if img.id in self.selected_images_id else None,
                    border_radius=3
                ))
        else:
            for img in images:
                self.grid.controls.append(
                    ft.Container(
                        content=ft.Image(src=ImageData.minio_link(img.thumbnail_object_name), expand=True, fit='cover'),
                        on_click=lambda _, image_id=img.id: self.page.go(f'/image/{image_id}'),
                        tooltip=f'{img.uploaded_at}\n{img.size} байт',
                    )
                )
        if update:
            self.grid.update()
