import flet as ft
from api.image_api import ImageApi
from api.images_api import images_api
from .base_view import BaseView

class ImageView(BaseView):
    ROUTE = '/image/:image_id'
    APP_BAR_TITLE_ROUTE = '/images'

    def __init__(self, page: ft.Page, image_id: int):
        super().__init__(page)
        self.image_id = image_id
        self.image_api = ImageApi(self.image_id)
        self.assemble_page()

    def assemble_page(self):
        self.controls = [self.get_image(),
                         self.get_scroll_images()]
    
    def tap_on_screen(self, e: ft.TapEvent, img):
        dlg = ft.AlertDialog(
            content=ft.Container(
                content=ft.Image(
                    src=img.img_to_base64(img.image_path),
                    expand=True,
                    fit='contain'
                ),
                expand=True,
            ),
            icon_padding=0,
            inset_padding=0,
            title_padding=0,
            actions_padding=0,
            content_padding=0,
            action_button_padding=0
        )
        self.page.open(dlg)

    def get_image(self):
        img = self.image_api.get_image()
        n_neighbors_images = images_api.get_n_neighbors(self.image_id, 1)
        image_index = n_neighbors_images.index(img)
        prev_image, next_image = None, None
        if image_index > 0:
            prev_image = n_neighbors_images[image_index - 1]
        if image_index < len(n_neighbors_images) - 1:
            next_image = n_neighbors_images[image_index + 1]
        return ft.Row(
            [
                ft.Container(
                    ft.IconButton(
                        icon=ft.Icons.ARROW_BACK,
                        expand=True,
                        disabled=prev_image,
                        on_click=lambda e: self.page.go(f'/image/{prev_image.id}'),
                    ) if prev_image else None,
                    expand=True
                ),
                ft.GestureDetector(
                    ft.Container(
                        ft.Image(src=img.img_to_base64(img.image_path), fit="contain"),
                        disabled=False,
                        expand=True,
                        alignment=ft.alignment.center
                    ),
                    on_tap_down=lambda e: self.tap_on_screen(e, img),
                ),
                ft.Container(
                    ft.IconButton(
                        icon=ft.Icons.ARROW_FORWARD,
                        expand=True,
                        disabled=next_image,
                        on_click=lambda e: self.page.go(f'/image/{next_image.id}'),
                    ) if next_image else None,
                    expand=True
                ),
            ],
            expand=True,
            # alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        )


    
    def get_scroll_images(self, n_neighbors=3):
        row = ft.Row(
            spacing=10,
            wrap=False,
            alignment=ft.MainAxisAlignment.CENTER,
        )
        n_neighbors_images = images_api.get_n_neighbors(self.image_id, n_neighbors)
        selected_index = n_neighbors_images.index(self.image_api)
        left_padding = max(0, n_neighbors - selected_index)
        right_padding = max(0, n_neighbors - (len(n_neighbors_images) - selected_index) + 1)

        row.controls.extend([ft.Container(width=70, height=70)] * left_padding)

        for img in n_neighbors_images:
            is_selected = self.image_api == img
            row.controls.append(
                ft.Container(
                    content=ft.Image(
                        src=img.img_to_base64(img.preview_path),
                        width=70 if not is_selected else 90,
                        height=70 if not is_selected else 90,
                        border_radius=5,
                        fit='cover',
                    ),
                    on_click=lambda _, image_id=img.id: self.page.go(f'/image/{image_id}'),
                    disabled=is_selected,
                    tooltip=f'{img.uploaded_at}\n{img.size} байт',
                    border=ft.border.all(3, ft.colors.BLUE) if is_selected else None,
                    border_radius=10,
                    padding=5,
                )
            )
        row.controls.extend([ft.Container(width=70, height=70, padding=5)] * right_padding)
        
        return row
