import flet as ft
from api.images_api import images_api
from .base_view import BaseView

class DeleteImagesView(BaseView):
    ROUTE = '/delete'
    IN_NAV_BAR = True
    NAV_BAR_POS = 2
    NAV_BAR_ICON = ft.Icons.DELETE
    NAV_BAR_LABEL = 'Удаление'

    def __init__(self, page: ft.Page):
        super().__init__(page)
        self.assemble_page()

    def assemble_page(self):
        self.expand_app_bar()
        self.grid = ft.GridView(runs_count=3, max_extent=140, spacing=10, expand=True)
        self.controls = [ft.Text('Кнопка удалить'), self.grid]
        self.load_grid()

    def load_grid(self):
        self.grid.controls.clear()
        for img in images_api.get_images():
            self.grid.controls.append(
                ft.Container(
                    content=ft.Image(src=img.img_to_base64(img.preview_path), expand=True, fit='cover'),
                    # on_click=lambda _, image_id=img.id: self.page.go(f'/image/{image_id}'),
                    tooltip=f'{img.uploaded_at}\n{img.size} байт',
                )
            )
        self.page.update()
    
    def expand_app_bar(self):
        def set_sorting_and_reload(self: DeleteImagesView, sort_by):
            images_api.set_sorting(sort_by=sort_by)
            self.load_grid()

        self.appbar.actions.append(ft.PopupMenuButton(
            items=[
                ft.PopupMenuItem(text="По дате", on_click=lambda e: set_sorting_and_reload(self, 'uploaded_at')),
                ft.PopupMenuItem(text="По размеру", on_click=lambda e: set_sorting_and_reload(self, 'size')),
            ],
            icon=ft.Icons.SORT,
            tooltip="Отсортировать"
        ))
