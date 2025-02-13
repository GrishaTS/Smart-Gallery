import flet as ft
from .base_view import BaseView

class DeleteImagesView(BaseView):
    def __init__(self, page):
        super().__init__('/delete', page)
    
        self.assemble_page()
    
    def assemble_page(self):
        self.controls = [ft.Text('delete')]