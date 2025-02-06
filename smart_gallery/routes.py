import flet as ft
from views.main_view import main_view
from views.image_view import image_view
from views.del_images_view import del_images_view


def setup_routes(page: ft.Page) -> None:
    '''Настраивает маршрутизацию для приложения.'''

    def on_route_change(event: ft.RouteChangeEvent) -> None:
        '''Обрабатывает изменение маршрута и загружает соответствующую страницу.'''
        page.views.clear()
        route_path = event.route.split('?')[0]

        routes = {
            '/': main_view,
            '/image': image_view,
            '/del_images': del_images_view,
        }

        new_view = ft.View(
            route=route_path,
            controls=[routes.get(route_path, lambda _: ft.Text('Страница не найдена'))(page)],
        )

        page.views.append(new_view)
        page.update()

    page.on_route_change = on_route_change
    page.go('/')
