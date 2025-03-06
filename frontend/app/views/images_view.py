import os
import uuid
import flet as ft
from api import images_api, ImageApi
from .base_view import BaseView
from .mixins import AppBarMixin, GridMixin, NavBarMixin

class ImagesView(BaseView, AppBarMixin, GridMixin, NavBarMixin):
    ROUTE = '/images'

    APP_BAR_TITLE_ROUTE = '/'
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
        self.controls = [self.grid,]
        self.load_grid(update=False)
        self.add_nav_bar()
    
    def get_images(self):
        return images_api.get_images()
        
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
