import flet as ft
from abc import ABC, abstractmethod

class BaseView(ft.View, ABC):
    ROUTE = None

    def __init__(self, page: ft.Page):
        super().__init__(self.ROUTE)
        self.page = page

    @abstractmethod
    def assemble_page(self):
        pass

    def super(self):
        print(self.__class__.__subclasses__)
