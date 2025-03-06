import flet as ft
from api.images_api import images_api
from .base_view import BaseView
from api.image_api import ImageApi

class DeleteImagesView(BaseView):
    ROUTE = '/delete'
    IN_NAV_BAR = True
    NAV_BAR_POS = 2
    NAV_BAR_ICON = ft.Icons.DELETE
    NAV_BAR_LABEL = 'Удаление'

    def __init__(self, page: ft.Page):
        super().__init__(page)
        self.selection_images_id = []
        self.assemble_page()

    def assemble_page(self):
        self.expand_app_bar()
        self.grid = ft.GridView(runs_count=3, max_extent=140, spacing=10, expand=True)
        self.controls = [self.grid]
        self.load_grid()
    
    def add_selection_image(self, image_id):
        if image_id in self.selection_images_id:
            self.selection_images_id.remove(image_id)
        else:
            self.selection_images_id.append(image_id)
        self.confirm_button.disabled = not bool(self.selection_images_id)
        self.confirm_button.bgcolor = ft.colors.RED_200 if self.confirm_button.disabled else ft.colors.RED
            
        self.load_grid()

    def load_grid(self):
        self.grid.controls.clear()
        for img in images_api.get_images():
            
            self.grid.controls.append(
                ft.Container(
                    content=ft.Image(src=img.img_to_base64(img.preview_path), expand=True, fit='cover'),
                    on_click=lambda _, image_id=img.id: self.add_selection_image(image_id),
                    tooltip=f'{img.uploaded_at}\n{img.size} байт',
                    border=ft.border.all(3, 'blue') if img.id in self.selection_images_id else None,
                    border_radius=3
                )
            )
        self.page.update()
    
    def confirm_deletion(self):
        for image_id in self.selection_images_id:
            ImageApi.delete_image(image_id)
        self.selection_images_id = []
        self.confirm_button.disabled = True
        self.confirm_button.bgcolor = ft.colors.RED_200
        self.load_grid()
    
    def delete_all(self):
        def cancel_delete(_):
            dialog.open = False
            self.page.update()

        def confirm_delete(_):
            images_api.delete_images()
            self.selection_images_id = []
            self.load_grid()
            dialog.open = False
            self.page.go('/images')

        dialog = ft.AlertDialog(
            title=ft.Text("Удаление всех изображений"),
            content=ft.Text("Вы уверены, что хотите удалить все изображения? Это действие необратимо."),
            actions=[
                ft.TextButton("Отмена", on_click=cancel_delete),
                ft.TextButton("Удалить", on_click=confirm_delete, style=ft.ButtonStyle(bgcolor=ft.colors.RED, color=ft.colors.WHITE)),
            ]
        )
        self.page.open(dialog)
        self.page.update()

    def expand_app_bar(self):
        def set_sorting_and_reload(self: DeleteImagesView, sort_by):
            images_api.set_sorting(sort_by=sort_by)
            self.load_grid()

        self.appbar.actions.insert(0, ft.PopupMenuButton(
            items=[
                ft.PopupMenuItem(text='По дате', on_click=lambda e: set_sorting_and_reload(self, 'uploaded_at')),
                ft.PopupMenuItem(text='По размеру', on_click=lambda e: set_sorting_and_reload(self, 'size')),
            ],
            icon=ft.Icons.SORT,
            tooltip='Отсортировать'
        ))
        
        self.delete_all_button = ft.IconButton(
            icon=ft.Icons.DELETE,
            on_click=lambda e: self.delete_all(),
            tooltip='Удалить все'
        )
        self.appbar.actions.insert(0, self.delete_all_button)

        self.confirm_button = ft.ElevatedButton(
            text='Подтвердить',
            on_click=lambda e: self.confirm_deletion(),
            icon=ft.icons.CHECK,
            bgcolor=ft.colors.RED_200,
            color=ft.colors.WHITE,
            icon_color=ft.colors.WHITE,
            style=ft.ButtonStyle(text_style=ft.TextStyle(
                weight=ft.FontWeight.BOLD,
            )),
            disabled=True
        )
        self.appbar.actions.insert(0, self.confirm_button)
