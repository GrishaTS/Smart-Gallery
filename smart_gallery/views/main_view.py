import flet as ft
import pickle
from utils.theme import toggle_theme
from utils.database import get_preview_list, insert_image
from utils.search_images import is_matching, txt_embedding


def main_view(page: ft.Page) -> ft.Column:
    'Главное окно приложения с отображением изображений, сортировкой, поиском и загрузкой.'
    page.clean()

    query_params = page.query.to_dict
    sort_order = query_params.get('sort', 'date_create')
    order_direction = query_params.get('order', 'DESC')

    images = get_preview_list(sort=sort_order, order=order_direction)

    def on_text_change(event: ft.ControlEvent) -> None:
        'Активирует кнопку поиска при вводе текста.'
        search_button.disabled = not bool(search_field.value)
        page.update()

    search_field = ft.TextField(
        label='Поиск изображений по описанию',
        expand=True,
        border_color='blue',
        border_width=1,
        focused_border_width=3,
        visible=False,
        on_change=on_text_change,
        on_submit=lambda _: filter_images(search_field.value),
    )

    def filter_images(txt):
        nonlocal images
        images = get_preview_list(sort=sort_order, order=order_direction)
        new_images = []
        txt_embed = txt_embedding(txt)

        for id, preview, emb_path, *_ in images:
            with open(emb_path, 'rb') as f:
                img_embed = pickle.load(f)
                similarity = is_matching(txt_embed, img_embed)
                new_images.append(((id, preview, emb_path, *_), similarity))
        sorted_new_images = sorted(new_images, key=lambda x: x[1], reverse=True)
        filtered_new_images = list(filter(lambda x: x[1] > 17.5, sorted_new_images))
        if not filter_images:
            images = [sorted_new_images[0]]
        else:
            images = filtered_new_images
        images = list(map(lambda x: x[0], images))
        update_image_grid()

    search_button = ft.ElevatedButton(
        'Найти',
        on_click=lambda _: filter_images(search_field.value),
        disabled=True,
        visible=False,
    )

    search_container = ft.Container(
        content=ft.Row([search_field, search_button], spacing=10),
        height=0,
        opacity=0,
        animate=ft.animation.Animation(300, 'easeInOut'),
    )

    def toggle_search(_: ft.ControlEvent) -> None:
        'Показывает/скрывает поле поиска.'
        nonlocal images
        if search_container.height == 0:
            search_field.visible = True
            search_button.visible = True
            search_container.height = 60
            search_container.opacity = 1
            search_button_control.icon = ft.icons.CLOSE
            search_field.focus()
        else:
            search_field.visible = False
            search_button.visible = False
            search_container.height = 0
            search_container.opacity = 0
            search_button_control.icon = ft.icons.SEARCH
            images = get_preview_list(sort_order, order_direction)
            update_image_grid()
        page.update()

    def order_by(column: str) -> None:
        'Изменяет порядок сортировки изображений.'
        nonlocal sort_order, order_direction, images
        if column == sort_order:
            order_direction = 'DESC' if order_direction == 'ASC' else 'ASC'
        else:
            sort_order = column
            order_direction = 'DESC'
        images = get_preview_list(sort=sort_order, order=order_direction)
        update_image_grid()

    sort_button = ft.PopupMenuButton(
        items=[
            ft.PopupMenuItem(text='По дате', on_click=lambda _: order_by('date_create')),
            ft.PopupMenuItem(text='По размеру', on_click=lambda _: order_by('size')),
        ],
        icon=ft.icons.SORT,
        tooltip='Отсортировать',
    )

    search_button_control = ft.IconButton(
        icon=ft.icons.SEARCH, on_click=toggle_search, tooltip='Поиск по описанию'
    )

    delete_button = ft.IconButton(
        ft.icons.DELETE_OUTLINE,
        on_click=lambda _: page.go('/del_images', sort=sort_order, order=order_direction),
        tooltip='Удалить',
    )

    def on_file_picked(event: ft.FilePickerResultEvent) -> None:
        'Обрабатывает загрузку изображений.'
        nonlocal images
        if event.files:
            for file in event.files:
                insert_image(file.path)
                images = get_preview_list(sort=sort_order, order=order_direction)
                update_image_grid()
                page.update()

    file_picker = ft.FilePicker(on_result=on_file_picked)
    page.overlay.append(file_picker)

    def update_image_grid() -> None:
        'Обновляет сетку изображений.'
        grid.controls.clear()
        for img_id, preview_img, embed_path, date_create, size in images:
            grid.controls.append(
                ft.Container(
                    content=ft.Image(src=preview_img, expand=True, fit='cover'),
                    on_click=lambda _, img=img_id: page.go(f'/image', img=img, sort=sort_order, order=order_direction),
                    tooltip=f'{date_create}\n{size} байт',
                )
            )
        page.update()

    grid = ft.GridView(runs_count=3, max_extent=140, spacing=10, expand=True)
    update_image_grid()

    layout = ft.Column(
        [
            ft.Row(
                [
                    ft.IconButton(ft.icons.BRIGHTNESS_4, on_click=toggle_theme, tooltip='Переключить тему'),
                    search_button_control,
                    ft.ElevatedButton(
                        'Найти дубликаты',
                        on_click=lambda _: print('Поиск дубликатов'),
                        color='white',
                        bgcolor='blue',
                    ),
                    ft.IconButton(
                        ft.icons.ADD,
                        on_click=lambda _: file_picker.pick_files(
                            allowed_extensions=['png', 'jpg', 'jpeg'], allow_multiple=True
                        ),
                        tooltip='Добавить',
                    ),
                    delete_button,
                    sort_button,
                ],
                alignment='spaceBetween',
            ),
            search_container,
            grid,
        ],
        spacing=20,
        expand=True,
    )

    page.add(layout)
    return layout
