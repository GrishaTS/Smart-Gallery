import flet as ft
from api import images_api, ImageApi
from .base_view import BaseView
from routes import ViewRoutes
from .mixins import AppBarMixin
from data import ImageData

class ImageView(BaseView, AppBarMixin):
    ROUTE = ViewRoutes.IMAGE

    APP_BAR_TITLE_ROUTE = ViewRoutes.IMAGES
    APP_BAR_THEME = True
    APP_BAR_DELETE = True

    def __init__(self, page: ft.Page, image_id):
        super().__init__(page)
        self.n_neighbors = int((self.page.width / 100 - 1) / 2)
        self.init_images(image_id)
        self.assemble_page()
    
    def init_images(self, image_id):
        self.cur_imgage = ImageApi.fetch_image(image_id)
        self.n_neighbors_images = images_api.get_n_neighbors(self.cur_imgage, self.n_neighbors)
        image_index = self.n_neighbors_images.index(self.cur_imgage)
        self.prev_image, self.next_image = None, None
        if image_index > 0:
            self.prev_image = self.n_neighbors_images[image_index - 1]
        if image_index < len(self.n_neighbors_images) - 1:
            self.next_image = self.n_neighbors_images[image_index + 1]
    
    def assemble_page(self):
        self.app_bar()
        self.page.on_keyboard_event = self.tap_on_key
        self.page.on_resized = self.update_n_neighbors
        self.scroller = ft.Row(
            spacing=10,
            wrap=False,
            alignment=ft.MainAxisAlignment.CENTER,
        )
        self.controls = [self.get_image(),
                         self.scroller]
        self.load_scroller_images(update=False)
    
    def tap_on_key(self, e: ft.KeyboardEvent):
        if e.key == 'Arrow Left' and self.prev_image:
            self.page.go(ViewRoutes.build(ViewRoutes.IMAGE, image_id=self.prev_image.id))
        elif e.key == 'Arrow Right' and self.next_image:
            self.page.go(ViewRoutes.build(ViewRoutes.IMAGE, image_id=self.next_image.id))

    def tap_on_image(self, e: ft.TapEvent, img: ImageData):
        dlg = ft.AlertDialog(
            content=ft.Container(
                content=ft.Image(
                    src=img.image_object_name,
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
    
    def update_n_neighbors(self, *_):
        self.n_neighbors = int((self.page.width / 100 - 1) / 2)
        self.load_scroller_images()

    def get_image(self):
        return ft.Row(
            [
                ft.Container(
                    ft.IconButton(
                        icon=ft.Icons.ARROW_BACK,
                        expand=True,
                        disabled=self.prev_image,
                        on_click=lambda e: self.page.go(ViewRoutes.build(ViewRoutes.IMAGE, image_id=self.prev_image.id)),
                    ) if self.prev_image else None,
                ),
                ft.Container(
                    content=ft.Image(src=ImageData.minio_link(self.cur_imgage.image_object_name), fit='contain'),
                    alignment=ft.alignment.center,
                    on_click=lambda e: self.tap_on_image(e, self.cur_imgage),
                    expand=True
                ),
                ft.Container(
                    ft.IconButton(
                        icon=ft.Icons.ARROW_FORWARD,
                        expand=True,
                        disabled=self.next_image,
                        on_click=lambda e: self.page.go(ViewRoutes.build(ViewRoutes.IMAGE, image_id=self.next_image.id)),
                    ) if self.next_image else None,
                ),
            ],
            expand=True,
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        )

    def load_scroller_images(self, update=True):
        if update:
            self.scroller.clean()
        selected_index = self.n_neighbors_images.index(self.cur_imgage)
        left_padding = max(0, self.n_neighbors - selected_index)
        right_padding = max(0, self.n_neighbors - (len(self.n_neighbors_images) - selected_index) + 1)

        self.scroller.controls.extend([ft.Container(width=70, height=70)] * left_padding)

        for img in self.n_neighbors_images:
            is_selected = self.cur_imgage == img
            self.scroller.controls.append(
                ft.Container(
                    content=ft.Image(
                        src=ImageData.minio_link(img.thumbnail_object_name),
                        width=70 if not is_selected else 90,
                        height=70 if not is_selected else 90,
                        border_radius=5,
                        fit='cover',
                    ),
                    on_click=lambda _, image_id=img.id: self.page.go(ViewRoutes.build(ViewRoutes.IMAGE, image_id=image_id)),
                    disabled=is_selected,
                    tooltip=f'{img.uploaded_at}\n{img.size} байт',
                    border=ft.border.all(3, ft.colors.BLUE) if is_selected else None,
                    border_radius=10,
                    padding=5,
                )
            )
        self.scroller.controls.extend([ft.Container(width=70, height=70, padding=5)] * right_padding)
        if update:
            self.scroller.update()
    
    def delete(self):
        ImageApi.delete_image(self.cur_imgage.id)
        if self.prev_image:
            self.page.go(ViewRoutes.build(ViewRoutes.IMAGE, image_id=self.prev_image.id))
        elif self.next_image:
            self.page.go(ViewRoutes.build(ViewRoutes.IMAGE, image_id=self.next_image.id))
        else:
            self.page.go(ViewRoutes.IMAGES)
