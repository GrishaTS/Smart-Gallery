import flet as ft
from utils.database import delete_image, get_preview_list, delete_all_images


def del_images_view(page: ft.Page) -> ft.Column:
    'Создаёт страницу для удаления изображений.'
    page.clean()

    query_params = page.query.to_dict
    sort_order = query_params.get('sort', 'date_create')
    sort_direction = query_params.get('order', 'DESC')

    images = get_preview_list(sort=sort_order, order=sort_direction)
    selected_images: set[int] = set()

    def delete_all(_: ft.ControlEvent) -> None:
        'Удаляет все изображения и возвращает на главную.'
        delete_all_images()
        page.go('/')

    def select_image(img_id: int) -> None:
        'Выбирает или снимает выбор с изображения.'
        if img_id in selected_images:
            selected_images.remove(img_id)
        else:
            selected_images.add(img_id)
        update_image_grid()
        page.update()

    def delete_selected_images(_: ft.ControlEvent) -> None:
        'Удаляет выбранные изображения и возвращает на главную.'
        for img_id in selected_images:
            delete_image(img_id)
        page.go('/')

    def update_image_grid() -> None:
        'Обновляет сетку изображений.'
        grid.controls.clear()
        for img_id, preview_img, *_ in images:
            grid.controls.append(
                ft.Container(
                    content=ft.Image(src=preview_img, expand=True, fit='cover'),
                    on_click=lambda _, img=img_id: select_image(img),
                    border=ft.border.all(4, 'blue' if img_id in selected_images else 'transparent'),
                )
            )

    cancel_button = ft.IconButton(
        ft.icons.CANCEL, on_click=lambda _: page.go('/'), tooltip='Отмена'
    )

    delete_all_button = ft.ElevatedButton(
        'Удалить все',
        on_click=delete_all,
        color='white',
        bgcolor='gray' if not images else 'blue',
    )

    final_delete_button = ft.IconButton(
        ft.icons.DELETE_OUTLINE, on_click=delete_selected_images, tooltip='Удалить'
    )

    grid = ft.GridView(
        runs_count=3,
        max_extent=140,
        spacing=10,
        expand=True,
    )

    update_image_grid()

    layout = ft.Column(
        [
            ft.Row(
                [cancel_button, delete_all_button, final_delete_button],
                alignment='spaceAround',
            ),
            grid,
        ],
        spacing=20,
        expand=True,
    )

    page.add(layout)
    return layout
