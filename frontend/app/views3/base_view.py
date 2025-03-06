import flet as ft
from abc import ABC, abstractmethod

from utils.theme import toggle_theme


class BaseView(ft.View, ABC):
    ROUTE = None
    APP_BAR_TITLE_ROUTE = '/'
    IN_NAV_BAR = False
    NAV_BAR_POS = None
    NAV_BAR_ICON = None
    NAV_BAR_LABEL = None

    def __init__(self, page: ft.Page):
        super().__init__(self.ROUTE)
        self.page = page
        self.add_app_bar()
        self.nav_bar_classes: list[BaseView] = sorted(
            filter(lambda cls_view: cls_view.IN_NAV_BAR, BaseView.__subclasses__()),
            key=lambda cls_view: cls_view.NAV_BAR_POS
        )
        if self.IN_NAV_BAR:
            self.add_nav_bar()

    @abstractmethod
    def assemble_page(self):
        'Этот метод собирает все control'
        pass

    def add_nav_bar(self):
        self.navigation_bar = ft.NavigationBar(
            destinations=[
                ft.NavigationBarDestination(icon=cls_view.NAV_BAR_ICON, label=cls_view.NAV_BAR_LABEL, tooltip='')
                for cls_view in self.nav_bar_classes
            ],
            on_change=lambda e: self.page.go(self.nav_bar_classes[e.control.selected_index].ROUTE),
            selected_index=self.nav_bar_classes.index(self.__class__)
        )
    
    def add_app_bar(self):
        if self.ROUTE == '/':
            span = ft.TextSpan(
                'Smart Gallery',
                style=ft.TextStyle(color=ft.colors.BLUE, weight='w500'),
                url='https://github.com/GrishaTS/Smart-Gallery',
            )
        else:
            span = ft.TextSpan(
                'Smart Gallery',
                style=ft.TextStyle(color=ft.colors.BLUE, weight='w500'),
                on_click=lambda e: self.page.go(self.APP_BAR_TITLE_ROUTE),
            )
        self.appbar = ft.AppBar(
            title=ft.Text(spans=[span]),
            center_title=False,
            actions=[
                ft.IconButton(ft.Icons.BRIGHTNESS_4, on_click=toggle_theme, tooltip='Переключить тему'),
            ],
        )
