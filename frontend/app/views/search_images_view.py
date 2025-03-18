import os
import uuid
from typing import Dict, List

import flet as ft

from app.api import images_api, ImageApi
from app.views.base_view import BaseView
from app.routes import ViewRoutes
from app.views.mixins import AppBarMixin, GridMixin, NavBarMixin


class SearchImagesView(BaseView, AppBarMixin, GridMixin, NavBarMixin):
    """
    Представление для поиска изображений по текстовому описанию.
    """

    ROUTE = ViewRoutes.SEARCH_IMAGES

    APP_BAR_TITLE_ROUTE = ViewRoutes.HOME
    APP_BAR_THEME = True
    APP_BAR_SEARCH = True

    NAV_BAR_POS = 1
    NAV_BAR_ICON = ft.Icons.SEARCH
    NAV_BAR_LABEL = "Поиск"

    def __init__(self, page: ft.Page):
        """
        Инициализирует страницу поиска изображений.

        :param page: Экземпляр страницы Flet.
        """
        self.map_uploads: Dict[str, str] = {}
        self.prompt: str = ""
        super().__init__(page)
        self.assemble_page()

    def assemble_page(self) -> None:
        """
        Собирает компоненты страницы.
        """
        self.app_bar()
        self.add_search_field()
        self.load_grid(update=False)
        self.set_visible_of_controls(update=False)
        self.controls = [self.search_field, self.grid]
        self.add_nav_bar()

    def set_visible_of_controls(self, update: bool = True) -> None:
        """
        Управляет видимостью элементов в зависимости от наличия результатов поиска.

        :param update: Флаг обновления элементов после изменения видимости.
        """
        self.grid.visible = bool(self.grid.controls)
        self.search_field.padding = 0 if self.grid.controls else 100

        if update:
            self.grid.update()
            self.search_field.update()

    def on_search_submit(self, e: ft.ControlEvent) -> None:
        """
        Обрабатывает отправку поискового запроса.

        :param e: Событие отправки запроса.
        """
        self.prompt = e.control.value.strip()
        if self.prompt:
            self.load_grid()
            self.set_visible_of_controls()

    def add_search_field(self) -> ft.Container:
        """
        Создаёт поле ввода для поиска изображений.

        :return: Flet контейнер с полем ввода.
        """
        self.search_field = ft.Container(
            content=ft.TextField(
                label="Поиск изображений по описанию",
                border_color="blue",
                border_width=1,
                focused_border_width=3,
                on_submit=self.on_search_submit,
            ),
            alignment=ft.alignment.center,
            padding=100,
        )
        return self.search_field

    def get_images(self) -> List:
        """
        Выполняет поиск изображений по текстовому описанию.

        :return: Список найденных изображений.
        """
        return images_api.search_images(self.prompt)

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
        if e.progress:
            ImageApi.post_image(self.map_uploads[e.file_name])
            self.load_grid()

    def on_files_picked(self, e: ft.FilePickerResultEvent) -> None:
        """
        Обрабатывает выбор файлов пользователем.

        :param e: Событие выбора файлов.
        """
        if not e.files:
            return

        self.map_uploads.clear()
        files = []

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

        self.file_picker.upload(files)
