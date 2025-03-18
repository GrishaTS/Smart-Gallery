from abc import ABC, abstractmethod
from typing import Optional

import flet as ft


class BaseView(ft.View, ABC):
    """
    Базовый класс представления в Flet-приложении.
    """

    ROUTE: Optional[str] = None

    def __init__(self, page: ft.Page):
        """
        Инициализирует представление.

        :param page: Экземпляр страницы Flet.
        """
        super().__init__(self.ROUTE)
        self.page = page

    @abstractmethod
    def assemble_page(self) -> None:
        """
        Абстрактный метод для сборки страницы.
        Должен быть реализован в наследуемых классах.
        """
        pass

    def super(self) -> None:
        """
        Выводит список подклассов текущего класса.
        """
        print(self.__class__.__subclasses__())
