import os
import uuid
from typing import Dict, List

import flet as ft

from app.api import images_api, ImageApi
from app.views.base_view import BaseView
from app.routes import ViewRoutes
from app.views.mixins import AppBarMixin, GridMixin, NavBarMixin


class ImagesView(BaseView, AppBarMixin, GridMixin, NavBarMixin):
    """
    Представление галереи изображений.
    """

    ROUTE = ViewRoutes.IMAGES

    APP_BAR_TITLE_ROUTE = ViewRoutes.HOME
    APP_BAR_THEME = True
    APP_BAR_SORTING = True
    APP_BAR_UPLOAD = True

    NAV_BAR_POS = 0
    NAV_BAR_ICON = ft.Icons.HOME
    NAV_BAR_LABEL = "Галерея"

    def __init__(self, page: ft.Page):
        """
        Инициализирует страницу галереи изображений.

        :param page: Экземпляр страницы Flet.
        """
        self.map_uploads: Dict[str, str] = {}
        self.count_files: int = 0
        super().__init__(page)
        self.assemble_page()

    def assemble_page(self) -> None:
        """
        Собирает компоненты страницы.
        """
        self.app_bar()
        self.main_upload_button()
        self.controls = [self.container_progress_ring, self.container_upload_button, self.grid]
        self.load_grid(update=False)
        self.add_nav_bar()

    def main_upload_button(self) -> None:
        """
        Создаёт основную кнопку загрузки изображений.
        """
        self.container_upload_button = ft.Container(
            ft.IconButton(
                ft.icons.UPLOAD_FILE,
                on_click=lambda e: self.file_picker.pick_files(
                    allowed_extensions=["png", "jpg", "jpeg"], allow_multiple=True
                ),
                tooltip="Добавить",
                icon_size=50,
            ),
            alignment=ft.alignment.center,
        )

    def load_grid(self, update: bool = True) -> None:
        """
        Загружает изображения в сетку.

        :param update: Флаг обновления сетки перед загрузкой.
        """
        super().load_grid(update)
        self.container_upload_button.visible = not bool(self.grid.controls)

        if update:
            self.container_upload_button.update()

    def get_images(self) -> List:
        """
        Получает список изображений.

        :return: Список объектов изображений.
        """
        return images_api.get_images()

    def set_sorting(self, sort_by: str) -> None:
        """
        Устанавливает сортировку изображений.

        :param sort_by: Поле для сортировки.
        """
        images_api.set_sorting(sort_by=sort_by)
        self.load_grid()

    def on_files_upload(self, e: ft.FilePickerUploadEvent) -> None:
        """
        Обрабатывает загрузку файлов.

        :param e: Событие загрузки файлов.
        """
        self.container_progress_ring.visible = True
        self.container_upload_button.visible = False

        if e.progress:
            self.progress_ring.value += 1 / self.count_files
            if round(self.progress_ring.value, 5) == 1:
                self.progress_ring.value = 0
                self.container_progress_ring.visible = False
                images_api.post_images([self.map_uploads[file.name] for file in self.file_picker.result.files])
                self.load_grid()

            self.container_progress_ring.update()

        self.container_upload_button.update()

    def on_files_picked(self, e: ft.FilePickerResultEvent) -> None:
        """
        Обрабатывает выбор файлов пользователем.

        :param e: Событие выбора файлов.
        """
        if not e.files:
            return

        files = []
        self.map_uploads.clear()

        for file in e.files:
            unique_name = f"{uuid.uuid4()}{os.path.splitext(file.name)[1].lower()}"
            self.map_uploads[file.name] = unique_name

            files.append(
                ft.FilePickerUploadFile(
                    file.name,
                    upload_url=self.page.get_upload_url(unique_name, 3600),
                    method="PUT",
                )
            )

        self.count_files = len(files)

        if self.count_files:
            self.file_picker.upload(files)
