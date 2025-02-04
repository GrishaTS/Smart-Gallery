import flet as ft
from views.main_view import main_view
from views.image_view import image_view
from views.del_images_view import del_images_view

def setup_routes(page: ft.Page):
    def on_route_change(e):
        page.views.clear()
        route_path = e.route.split('?')[0]

        routes = {
            '/': main_view,
            '/image': image_view,
            '/del_images': del_images_view,
        }

        if route_path in routes:
            new_view = ft.View(route=route_path, controls=[routes[route_path](page)])
        else:
            new_view = ft.View(route=route_path, controls=[ft.Text('Страница не найдена')])

        page.views.append(new_view)
        page.update()

    page.on_route_change = on_route_change
    page.go('/')
