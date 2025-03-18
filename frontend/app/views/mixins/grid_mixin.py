from abc import ABC, abstractmethod
from typing import List

import flet as ft

from app.data import ImageData


class GridMixin(ABC):
    """Миксин для работы с GridView в Flet-приложении."""

    GRID_SELECTION_MODE: bool = False

    def __init__(self):
        """
        Инициализация миксина.
        """
        self.grid = ft.GridView(runs_count=3, max_extent=140, spacing=10, expand=True)
        self.selected_images_id: List[int] = []
        super().__init__()
        self.page: ft.Page

    @abstractmethod
    def get_images(self) -> List[ImageData]:
        """
        Абстрактный метод для получения списка изображений.

        :return: Список объектов ImageData.
        """
        pass

    def load_grid(self, update: bool = True) -> None:
        """
        Загружает изображения в GridView.

        :param update: Флаг очистки GridView перед загрузкой.
        """
        if update:
            self.grid.clean()

        images: List[ImageData] = self.get_images()

        if self.GRID_SELECTION_MODE:
            if not hasattr(self, "add_selection_image"):
                raise AttributeError("Метод add_selection_image не инициализирован")

            for img in images:
                self.grid.controls.append(
                    ft.Container(
                        content=ft.Image(
                            src=ImageData.minio_link(img.thumbnail_object_name),
                            expand=True,
                            fit="cover",
                        ),
                        on_click=lambda _, image_id=img.id: self.add_selection_image(image_id),
                        tooltip=f"{img.uploaded_at}\n{img.size} байт",
                        border=ft.border.all(3, "blue") if img.id in self.selected_images_id else None,
                        border_radius=3,
                    )
                )
        else:
            for img in images:
                self.grid.controls.append(
                    ft.Container(
                        content=ft.Image(
                            src=ImageData.minio_link(img.thumbnail_object_name),
                            expand=True,
                            fit="cover",
                        ),
                        on_click=lambda _, image_id=img.id: self.page.go(f"/image/{image_id}"),
                        tooltip=f"{img.uploaded_at}\n{img.size} байт",
                    )
                )

        if update:
            self.grid.update()
