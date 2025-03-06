import os
import uuid
import flet as ft
from api.images_api import images_api
from api.image_api import ImageApi
from .base_view import BaseView
from config import settings

class ImagesView(BaseView):
    ROUTE = '/images'
    APP_BAR = True
    IN_NAV_BAR = True
    NAV_BAR_POS = 0
    NAV_BAR_ICON = ft.Icons.HOME
    NAV_BAR_LABEL = 'Галерея'

    def __init__(self, page: ft.Page):
        super().__init__(page)
        self.assemble_page()

    def assemble_page(self):
        self.expand_app_bar()
        self.grid = ft.GridView(runs_count=3, max_extent=140, spacing=10, expand=True)
        self.main_upload_button = ft.Container(
            self.get_upload_button(50),
            alignment=ft.alignment.center,
            expand=True,
        )
        self.map_uploads = {}
        self.controls = [self.main_upload_button,
                         self.grid,]
        self.load_grid(update=False)

    def load_grid(self, update=True):
        self.grid.controls.clear()
        images = images_api.get_images()
        if not images:
            self.main_upload_button.visible = True
            self.grid.visible = False
            return
        self.main_upload_button.visible = False
        self.grid.visible = True
        for img in images:
            self.grid.controls.append(
                ft.Container(
                    content=ft.Image(src=img.img_to_base64(img.preview_path), expand=True, fit='cover'),
                    on_click=lambda _, image_id=img.id: self.page.go(f'/image/{image_id}'),
                    tooltip=f'{img.uploaded_at}\n{img.size} байт',
                )
            )
        if update:
            self.grid.update()
            self.main_upload_button.update()
    
    def expand_app_bar(self):

        def set_sorting_and_reload(self: ImagesView, sort_by):
            images_api.set_sorting(sort_by=sort_by)
            self.load_grid()
        self.appbar.actions.insert(0, ft.PopupMenuButton(
            items=[ft.PopupMenuItem(text='По дате', on_click=lambda e: set_sorting_and_reload(self, 'uploaded_at')),
                   ft.PopupMenuItem(text='По размеру', on_click=lambda e: set_sorting_and_reload(self, 'size'))],
            icon=ft.Icons.SORT,
            tooltip='Отсортировать'
        ))

        self.appbar.actions.insert(0, self.get_upload_button())
    
    def get_upload_button(self, icon_size=None):
        def on_files_upload(e: ft.FilePickerUploadEvent):
            if e.progress:
                ImageApi.post_image(self.map_uploads[e.file_name])
                self.load_grid()
        def on_files_picked(e: ft.FilePickerResultEvent):
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
            file_picker.upload(files)
        file_picker = ft.FilePicker(on_result=on_files_picked, on_upload=on_files_upload)
        self.page.overlay.append(file_picker)
        return ft.IconButton(
            ft.icons.UPLOAD_FILE,
            on_click=lambda e: file_picker.pick_files(allowed_extensions=['png', 'jpg', 'jpeg'],
                                                      allow_multiple=True),
            tooltip='Добавить',
            icon_size=icon_size,
        )
