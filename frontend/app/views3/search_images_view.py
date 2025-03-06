import flet as ft
from .base_view import BaseView

class SearchImagesView(BaseView):
    ROUTE = '/search'
    IN_NAV_BAR = True
    NAV_BAR_POS = 1
    NAV_BAR_ICON = ft.Icons.SEARCH
    NAV_BAR_LABEL = 'Поиск'

    def __init__(self, page):
        super().__init__(page)
        self.assemble_page()
    
    def assemble_page(self):
        self.controls = [ft.Text('search')]