import flet as ft
from abc import ABC, abstractmethod

class BaseView(ft.View, ABC):
    def __init__(self, route: str, page: ft.Page):
        super().__init__(route)

        self.page = page
        self.navigation_bar = ft.NavigationBar(
            destinations=[
                ft.NavigationBarDestination(icon=ft.Icons.HOME, label='Галерея'),
                ft.NavigationBarDestination(icon=ft.Icons.SEARCH, label='Поиск'),
                ft.NavigationBarDestination(icon=ft.Icons.DELETE, label='Удаление'),
            ],
            on_change=lambda e: page.go(['/', '/search', '/delete'][e.control.selected_index]),
            selected_index=['/', '/search', '/delete'].index(route)
        )

    @abstractmethod
    def assemble_page(self):
        'Этот метод собирает все control'
        pass