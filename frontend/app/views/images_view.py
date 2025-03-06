import time
from copy import deepcopy
import os
import uuid
import flet as ft
from api import images_api, ImageApi
from .base_view import BaseView
from routes import ViewRoutes
from .mixins import AppBarMixin, GridMixin, NavBarMixin

class ImagesView(BaseView, AppBarMixin, GridMixin, NavBarMixin):
    ROUTE = ViewRoutes.IMAGES

    APP_BAR_TITLE_ROUTE = ViewRoutes.HOME
    APP_BAR_THEME = True
    APP_BAR_SORTING = True
    APP_BAR_UPLOAD = True
    
    NAV_BAR_POS = 0
    NAV_BAR_ICON = ft.Icons.HOME
    NAV_BAR_LABEL = 'Галерея'

    def __init__(self, page: ft.Page):
        self.map_uploads = {}
        super().__init__(page)
        self.assemble_page()
    
    def assemble_page(self):
        self.app_bar()
        self.main_upload_button()
        self.controls = [self.container_progress_ring,
                         self.container_upload_button,
                         self.grid]
        self.load_grid(update=False)
        self.add_nav_bar()

    def main_upload_button(self):
        self.container_upload_button = ft.Container(ft.IconButton(
            ft.icons.UPLOAD_FILE,
            on_click=lambda e: self.file_picker.pick_files(allowed_extensions=['png', 'jpg', 'jpeg'],
                                                      allow_multiple=True),
            tooltip='Добавить',
            icon_size=50,
        ), alignment=ft.alignment.center)
    
    def load_grid(self, update=True):
        super().load_grid(update)
        if self.grid.controls:
            self.container_upload_button.visible = False
        else:
            self.container_upload_button.visible = True
        if update:
            self.container_upload_button.update()
    
    def get_images(self):
        return images_api.get_images()
        
    def set_sorting(self, sort_by):
        images_api.set_sorting(sort_by=sort_by)
        self.load_grid()
    
    def on_files_upload(self, e: ft.FilePickerUploadEvent):
        self.container_progress_ring.visible = True
        self.container_upload_button.visible = False
        if e.progress:
            self.progress_ring.value += 1 / self.count_files
            if round(self.progress_ring.value, 5) == 1:
                self.progress_ring.value = 0
                self.container_progress_ring.visible = False
                images_api.post_images([self.map_uploads[file.name] for file
                                        in self.file_picker.result.files])
                self.load_grid()
            self.container_progress_ring.update()
        self.container_upload_button.update()

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
        self.count_files = len(files)
        if self.count_files:
            self.file_picker.upload(files)
