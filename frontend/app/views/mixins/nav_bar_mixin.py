from typing import List, Type

import flet as ft


class NavBarMixin:
    """
    Миксин для добавления навигационной панели в Flet-приложение.
    """

    NAV_BAR_POS: int
    NAV_BAR_ICON: ft.Icon
    NAV_BAR_LABEL: str
    ROUTE: str

    def __init__(self):
        """
        Инициализация миксина.
        """
        super().__init__()
        self.page: ft.Page
        self.nav_bar_classes: List[Type["NavBarMixin"]] = []

    def add_nav_bar(self) -> None:
        """
        Создаёт и добавляет навигационную панель.
        """
        self.nav_bar_classes = sorted(
            NavBarMixin.__subclasses__(),
            key=lambda cls: cls.NAV_BAR_POS,
        )

        self.navigation_bar = ft.NavigationBar(
            destinations=[
                ft.NavigationBarDestination(
                    icon=cls.NAV_BAR_ICON, label=cls.NAV_BAR_LABEL, tooltip=""
                )
                for cls in self.nav_bar_classes
            ],
            selected_index=self.nav_bar_classes.index(self.__class__),
            on_change=self.on_nav_change,
        )

    def on_nav_change(self, e: ft.ControlEvent) -> None:
        """
        Обрабатывает изменение выбора в навигационной панели.

        :param e: Событие изменения выбора.
        """
        selected_class: Type["NavBarMixin"] = self.nav_bar_classes[e.control.selected_index]
        self.page.go(selected_class.ROUTE)
