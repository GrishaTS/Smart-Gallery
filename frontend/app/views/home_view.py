import flet as ft
from .base_view import BaseView

class HomeView(BaseView):
    ROUTE = '/'

    def __init__(self, page: ft.Page):
        super().__init__(page)
        self.assemble_page()

    def assemble_page(self):
        self.controls = [ft.TextButton('/images', on_click=lambda e: self.page.go('/images'))]
