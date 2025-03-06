import flet as ft
from .base_view import BaseView
from .mixins import AppBarMixin
from .images_view import ImagesView

class HomeView(BaseView, AppBarMixin):
    ROUTE = '/'

    def __init__(self, page: ft.Page):
        super().__init__(page)
        self.assemble_page()

    def assemble_page(self):
        self.app_bar()
        self.controls = [ft.Text('Описание проекта и ссылка главную страницу'),
                         ft.TextButton('/images', on_click=lambda e: self.page.go(ImagesView.ROUTE))]
