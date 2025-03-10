import os
import uuid
import flet as ft
from api import images_api, ImageApi
from .base_view import BaseView
from routes import ViewRoutes
from .mixins import AppBarMixin, GridMixin, NavBarMixin

class SearchImagesView(BaseView, AppBarMixin, GridMixin, NavBarMixin):
    ROUTE = ViewRoutes.SEARCH_IMAGES

    APP_BAR_TITLE_ROUTE = ViewRoutes.HOME
    APP_BAR_THEME = True
    APP_BAR_SEARCH = True
    
    NAV_BAR_POS = 1
    NAV_BAR_ICON = ft.Icons.SEARCH
    NAV_BAR_LABEL = 'Поиск'

    def __init__(self, page: ft.Page):
        self.map_uploads = {}
        self.prompt = ""
        super().__init__(page)
        self.assemble_page()
    
    def assemble_page(self):
        self.app_bar()
        self.add_search_field()
        self.load_grid(update=False)
        self.set_visible_of_controls()
        self.controls = [self.search_field, self.grid]
        self.add_nav_bar()
    
    def set_visible_of_controls(self):
        if self.grid.controls:
            self.grid.visible = True
            self.search_field.padding = 0
        else:
            self.grid.visible = False
            self.search_field.padding = 100
    
    def on_search_submit(self, e: ft.ControlEvent):
        self.prompt = e.control.value.strip()
        if self.prompt:
            self.load_grid()

    def add_search_field(self):
        self.search_field = ft.Container(
            content=ft.TextField(
            label="Поиск изображений по описанию",
            border_color='blue', border_width=1, focused_border_width=3,
            on_submit=self.on_search_submit,
        ),
            alignment=ft.alignment.center,
            padding=100
        )
        return self.search_field
    
    def get_images(self):
        return images_api.search_images(self.prompt)

    def set_sorting(self, sort_by):
        images_api.set_sorting(sort_by=sort_by)
        self.load_grid()
    
    def on_files_upload(self, e: ft.FilePickerUploadEvent):
        if e.progress:
            ImageApi.post_image(self.map_uploads[e.file_name])
            self.load_grid()

    def on_files_picked(self, e: ft.FilePickerResultEvent):
        files = []
        self.map_uploads = {}
        if not e.files:
            return
        for file in e.files:
            self.map_uploads[file.name] = f'{uuid.uuid4()}{os.path.splitext(file.name)[1].lower()}'
            files.append(
                ft.FilePickerUploadFile(
                    file.name,
                    upload_url=self.page.get_upload_url(self.map_uploads[file.name], 3600),
                    method='PUT'
                )
            )
        self.file_picker.upload(files)
