import flet as ft
from .base_view import BaseView

class ImageView(BaseView):
    def __init__(self, page):
        super().__init__('/image', page)

        self.assemble_page()
    
    def assemble_page(self):
        self.controls = [ft.Text('image')]