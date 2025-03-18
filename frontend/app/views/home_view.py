import flet as ft

from app.views.base_view import BaseView
from app.views.mixins import AppBarMixin
from app.views.images_view import ImagesView


class HomeView(BaseView, AppBarMixin):
    """
    Главная страница приложения.
    """

    ROUTE = "/"

    def __init__(self, page: ft.Page):
        """
        Инициализирует главную страницу.

        :param page: Экземпляр страницы Flet.
        """
        super().__init__(page)
        self.assemble_page()

    def assemble_page(self) -> None:
        """
        Собирает компоненты главной страницы.
        """
        self.app_bar()
        self.controls = [
            ft.Text("Описание проекта и ссылка на галерею изображений"),
            ft.TextButton("/images", on_click=lambda e: self.page.go(ImagesView.ROUTE)),
        ]
