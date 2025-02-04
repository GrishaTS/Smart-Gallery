import flet as ft
from utils.theme import toggle_theme
from utils.database import get_image_by_id, get_image_list, delete_image, get_adjacent_images


def image_view(page: ft.Page) -> ft.Column:
    '''Отображает страницу просмотра изображения с возможностью навигации и удаления.'''
    page.clean()

    query_params = page.query
    image_id = query_params.get('img')
    sort_order = query_params.get('sort')
    order_direction = query_params.get('order')

    if not all([image_id, sort_order, order_direction]):
        page.go('/')
        return ft.Column([])

    image_path = get_image_by_id(image_id)
    adjacent_images = get_adjacent_images(image_id, sort_order, order_direction)

    def handle_tap(event: ft.TapEvent) -> None:
        '''Обрабатывает нажатия на изображение для перехода между изображениями.'''
        tap_x = event.local_x
        screen_width = page.width

        if adjacent_images['previous'] and tap_x < screen_width * 0.2:
            page.go(f'/image', img=adjacent_images['previous'], sort=sort_order, order=order_direction)
        elif adjacent_images['next'] and tap_x > screen_width * 0.8:
            page.go(f'/image', img=adjacent_images['next'], sort=sort_order, order=order_direction)

    def delete_current_image(_: ft.ControlEvent) -> None:
        '''Удаляет текущее изображение и возвращает на главную страницу.'''
        delete_image(image_id)
        page.go('/')

    def handle_keyboard(event: ft.KeyboardEvent) -> None:
        '''Обрабатывает клавиши для навигации между изображениями.'''
        if event.key == 'Arrow Left':
            page.go(f'/image', img=adjacent_images['previous'], sort=sort_order, order=order_direction)
        elif event.key == 'Arrow Right':
            page.go(f'/image', img=adjacent_images['next'], sort=sort_order, order=order_direction)
        elif event.key == 'Escape':
            page.go('/')

    page.on_keyboard_event = handle_keyboard

    return ft.Column(
        [
            ft.Row(
                [
                    ft.IconButton(ft.icons.ARROW_BACK, on_click=lambda _: page.go('/'), tooltip='Назад'),
                    ft.IconButton(ft.icons.DELETE, on_click=delete_current_image, tooltip='Удалить'),
                    ft.IconButton(ft.icons.BRIGHTNESS_4, on_click=toggle_theme, tooltip='Переключить тему'),
                ],
                alignment='spaceBetween',
            ),
            ft.Container(
                content=ft.GestureDetector(
                    content=ft.Image(
                        src=image_path,
                        fit='contain',
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
