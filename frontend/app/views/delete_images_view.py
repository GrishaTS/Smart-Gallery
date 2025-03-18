import flet as ft
from typing import List

from app.api import images_api, ImageApi
from app.views.base_view import BaseView
from app.routes import ViewRoutes
from app.views.mixins import AppBarMixin, GridMixin, NavBarMixin


class DeleteImagesView(BaseView, AppBarMixin, GridMixin, NavBarMixin):
    """
    Представление для удаления изображений.
    """

    ROUTE = ViewRoutes.DELETE_IMAGES

    APP_BAR_TITLE_ROUTE = ViewRoutes.HOME
    APP_BAR_THEME = True
    APP_BAR_SORTING = True
    APP_BAR_DELETE = True
    APP_BAR_CONFIRM_DELETION = True

    NAV_BAR_POS = 2
    NAV_BAR_ICON = ft.Icons.DELETE
    NAV_BAR_LABEL = "Удаление"

    GRID_SELECTION_MODE = True

    def __init__(self, page: ft.Page):
        """
        Инициализирует страницу удаления изображений.

        :param page: Экземпляр страницы Flet.
        """
        super().__init__(page)
        self.assemble_page()

    def assemble_page(self) -> None:
        """
        Собирает компоненты страницы.
        """
        self.app_bar()
        self.controls = [self.grid]
        self.load_grid(update=False)
        self.add_nav_bar()

    def get_images(self):
        """
        Получает список изображений.

        :return: Список объектов ImageData.
        """
        return images_api.get_images()

    def set_sorting(self, sort_by: str) -> None:
        """
        Устанавливает сортировку изображений.

        :param sort_by: Поле, по которому нужно сортировать.
        """
        images_api.set_sorting(sort_by=sort_by)
        self.load_grid()

    def delete(self):
        """
        Открывает диалоговое окно подтверждения удаления всех изображений.
        """
        def cancel_delete(_):
            dialog.open = False
            self.page.update()

        def confirm_delete(_):
            images_api.delete_images()
            self.selected_images_id = []
            self.load_grid()
            dialog.open = False
            self.page.go(ViewRoutes.IMAGES)

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
    

    def confirm_deletion(self) -> None:
        """
        Подтверждает удаление выбранных изображений.
        """
        for image_id in self.selected_images_id:
            ImageApi.delete_image(image_id)

        self.selected_images_id.clear()
        self.confirm_deletion_button.disabled = True
        self.confirm_deletion_button.bgcolor = ft.colors.RED_200
        self.confirm_deletion_button.update()
        self.load_grid()

    def add_selection_image(self, image_id: int) -> None:
        """
        Добавляет или удаляет изображение из списка выбранных.

        :param image_id: ID изображения.
        """
        if image_id in self.selected_images_id:
            self.selected_images_id.remove(image_id)
        else:
            self.selected_images_id.append(image_id)

        self.confirm_deletion_button.disabled = not bool(self.selected_images_id)
        self.confirm_deletion_button.bgcolor = (
            ft.colors.RED_200 if self.confirm_deletion_button.disabled else ft.colors.RED
        )
        self.confirm_deletion_button.update()
        self.load_grid()
