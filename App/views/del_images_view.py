import os
import flet as ft
from config import IMAGES_DIR
from utils.database import delete_image, get_preview_list, delete_all_images

def del_images_view(page: ft.Page):
    page.clean()

    query_params = page.query.to_dict
    page.sort = query_params.get("sort", 'date_create')
    page.order = query_params.get("order", 'DESC')
    
    page.images = get_preview_list(sort=page.sort, order=page.order)

    selected_images = set()
    page.cancel_button = ft.IconButton(
        ft.icons.CANCEL,
        on_click=lambda e: page.go('/'),
        tooltip='Отмена'
    )
    page.final_delete_button = ft.IconButton(
        ft.icons.DELETE_OUTLINE,
        on_click=lambda e: delete_selected_images(page),
        tooltip='Удалить'
    )
    page.delete_all_button = ft.ElevatedButton(
        "Удалить все",
        on_click=lambda e: delete_all(e),
        color="white",
        bgcolor="gray" if len(page.images) == 0 else "blue",
    )

    def delete_all(e):
        delete_all_images()
        page.go('/')


    def select_image(img_id):
        if img_id in selected_images:
            selected_images.remove(img_id)
        else:
            selected_images.add(img_id)
        update_image_grid(page)
        page.update()
        

    def delete_selected_images(page):
        for img_id in selected_images:
            delete_image(img_id)  # Удаляем из базы данных
        page.go('/')
    
    def update_image_grid(page):
        # Очищаем текущую сетку
        page.controls[0].controls[1].controls.clear()
        # Добавляем новые изображения в сетку
        for id, preview_img, date_create, size in page.images:
            page.controls[0].controls[1].controls.append(
                ft.Container(
                    content=ft.Image(src=preview_img, expand=True, fit="cover"),
                    on_click=lambda e, img=id: select_image(img),
                    border=ft.border.all(4, "blue" if id in selected_images else "transparent")
                )
            )


    window = (
        ft.Column(
            [
                ft.Row(
                    [
                        page.cancel_button,
                        page.delete_all_button,
                        page.final_delete_button,
                    ],
                    alignment="spaceAround",
                ),
                ft.GridView(
                    [
                        ft.Container(
                            content=ft.Image(src=preview_img, expand=True, fit="cover"),
                            on_click=lambda e, img=id: select_image(img),
                            border=ft.border.all(4, "blue" if id in selected_images else "transparent")
                        )
                        for id, preview_img, date_create, size in page.images
                    ],
                    runs_count=3,
                    max_extent=140,
                    spacing=10,
                    expand=True,
                ),
            ],
            spacing=20,
            expand=True,
        )
    )
    page.add(window)
    return window