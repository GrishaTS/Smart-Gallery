import os
import flet as ft
from config import IMAGES_DIR
from controllers.navigation import navigate_image
from utils.theme import toggle_theme
from utils.database import get_image_by_id, get_image_list, delete_image, get_adjacent_images

def image_view(page: ft.Page):
    page.clean()
    page.images = get_image_list()
    query_params = page.query # Получаем параметры из URL
    image_id = query_params.get("img")
    page.sort = query_params.get("sort")
    page.order = query_params.get("order")
    if not all([image_id, page.sort, page.order]):
        page.go('/')

    image_path = get_image_by_id(image_id)

    page.adjacent_images = get_adjacent_images(image_id, page.sort, page.order)

    def handle_tap(e: ft.TapEvent):
        tap_x = e.local_x
        screen_width = page.width
        if page.adjacent_images['previous'] and tap_x < screen_width * 0.2:
            page.go(f"/image", img=page.adjacent_images['previous'], sort=page.sort, order=page.order)
        elif page.adjacent_images['next'] and tap_x > screen_width * 0.8:
            page.go(f"/image", img=page.adjacent_images['next'], sort=page.sort, order=page.order)
    
    def delete():
        delete_image(image_id)
        page.go('/')
    
    def on_keyboard(e: ft.KeyboardEvent):
        if e.key == "Arrow Left":
            page.go(f"/image", img=page.adjacent_images['previous'], sort=page.sort, order=page.order)
        elif e.key == "Arrow Right":
            page.go(f"/image", img=page.adjacent_images['next'], sort=page.sort, order=page.order)
        elif e.key == "Escape":
            page.go(f'/', sort=page.sort, order=page.order)

    page.on_keyboard_event = on_keyboard

    return (
        ft.Column(
            [
                ft.Row(
                    [
                        ft.IconButton(ft.icons.ARROW_BACK, on_click=lambda e: page.go('/'), tooltip='Назад'),
                        ft.IconButton(ft.icons.DELETE, on_click=lambda e: delete(), tooltip='Удалить'),
                        ft.IconButton(ft.icons.BRIGHTNESS_4, on_click=toggle_theme, tooltip='Переключить тему'),
                    ],
                    alignment="spaceBetween",
                ),
                ft.Container(
                    content=ft.GestureDetector(
                        content=ft.Image(
                            src=image_path,
                            fit="contain",
                            width=page.width,
                            height=page.height - 100,
                        ),
                        on_tap_down=handle_tap,
                    ),
                    expand=True,
                    alignment=ft.alignment.center,
                ),
            ],
            spacing=20,
            expand=True,
        )
    )
