import flet as ft
from .base_view import BaseView

class SearchImagesView(BaseView):
    def __init__(self, page):
        super().__init__('/search', page)
        
        self.assemble_page()
    
    def assemble_page(self):
        self.controls = [ft.Text('search')]