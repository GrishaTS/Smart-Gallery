import flet as ft
from utils.theme import toggle_theme
from utils.search import on_text_change
from utils.database import get_preview_list, insert_image

def main_view(page: ft.Page):
    page.clean()

    query_params = page.query.to_dict
    page.sort = query_params.get("sort", 'date_create')
    page.order = query_params.get("order", 'DESC')

    page.images = get_preview_list(sort=page.sort, order=page.order)
    page.search_field = ft.TextField(
        label="Поиск изображений по описанию",
        expand=True,
        border_color='blue', border_width=1, focused_border_width=3,
        visible=False,
        on_change=on_text_change
    )

    # Кнопка поиска
    page.search_button = ft.ElevatedButton(
        "Найти",
        on_click=lambda e: print(f"Поиск: {page.search_field.value}"),
        disabled=True,
        visible=False
    )
    page.search_container = ft.Container(
        content=ft.Row(
            [
                page.search_field,
                page.search_button,
            ],
            spacing=10,
        ),
        height=0,
        opacity=0,
        animate=ft.animation.Animation(300, "easeInOut"),
    )

    def toggle_search(e):
        if page.search_container.height == 0:
            page.search_field.visible = True
            page.search_button.visible = True
            page.search_container.height = 60
            page.search_container.opacity = 1
            page.search_button_control.icon = ft.Icons.CLOSE  # Иконка для скрытия
        else:
            page.search_field.visible = False
            page.search_button.visible = False
            page.search_container.height = 0
            page.search_container.opacity = 0
            page.search_button_control.icon = ft.Icons.SEARCH  # Иконка для поиска
        page.update()
    
    def order_by(column):
        if column == page.sort:
            page.order = 'DESC' if page.order == 'ASC' else 'ASC'
        else:
            page.sort = column
            page.order = 'DESC'
        page.images = get_preview_list(sort=page.sort, order=page.order)
        update_image_grid(page)
        page.update()

    page.sort_button = ft.PopupMenuButton(
        items=[
            ft.PopupMenuItem(text="По дате", on_click=lambda e: order_by('date_create')),
            ft.PopupMenuItem(text="По размеру", on_click=lambda e: order_by('size')),
        ],
        icon=ft.Icons.SORT,
        tooltip="Отсортировать"
    )

    page.search_button_control = ft.IconButton(
        icon=ft.icons.SEARCH,
        on_click=toggle_search,
        tooltip="Поиск по описанию"
    )

    page.delete_button = ft.IconButton(
        ft.icons.DELETE_OUTLINE,
        on_click=lambda e: page.go('/del_images', sort=page.sort, order=page.order),
        tooltip='Удалить'
    )

    def on_file_picked(e, page):
        if e.files:
            for file in e.files:
                insert_image(file.path)  # Вставляем в базу данных
                page.images = get_preview_list(sort=page.sort, order=page.order)
                update_image_grid(page)
                page.update()

    file_picker = ft.FilePicker(on_result=lambda e: on_file_picked(e, page))
    page.overlay.append(file_picker)

    def update_image_grid(page):
        # Очищаем текущую сетку
        page.controls[0].controls[2].controls.clear()
        
        # Добавляем новые изображения в сетку
        for id, preview_img, date_create, size in page.images:
            page.controls[0].controls[2].controls.append(
                ft.Container(
                    content=ft.Image(src=preview_img, expand=True, fit="cover"),
                    on_click=lambda e, img=id: page.go(f"/image", img=img, sort=page.sort, order=page.order),
                    tooltip=f'{date_create}\n{size} байт'
                )
            )

    window = (
        ft.Column(
            [
                ft.Row(
                    [
                        ft.IconButton(ft.icons.BRIGHTNESS_4, on_click=toggle_theme, tooltip="Переключить тему"),
                        page.search_button_control,
                        ft.ElevatedButton(
                            "Найти дубликаты",
                            on_click=lambda e: print("Поиск дубликатов"),
                            color="white",
                            bgcolor="gray" if len(page.images) == 0 else "blue",
                        ),
                        ft.IconButton(ft.icons.ADD, on_click=lambda e: file_picker.pick_files(allowed_extensions=["png", "jpg", "jpeg"], allow_multiple=True), tooltip="Добавить"),
                        page.delete_button,
                        page.sort_button,
                    ],
                    alignment="spaceBetween",
                ),
                page.search_container,
                ft.GridView(
                    [
                        ft.Container(
                            content=ft.Image(src=preview_img, expand=True, fit="cover"),
                            on_click=lambda e, img=id: page.go(f"/image", img=img, sort=page.sort, order=page.order),
                            tooltip=f'{date_create}\n{size} байт'
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