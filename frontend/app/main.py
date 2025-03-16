import os
import flet as ft
from config import settings
from views import (
    HomeView,
    ImagesView,
    SearchImagesView,
    DeleteImagesView,
    ImageView,
)

def main(page: ft.Page):
    page.title = 'Умная галерея'
    page.theme_mode = ft.ThemeMode.SYSTEM
    page.padding = 20
    page.window.min_width = 400
    page.window.min_height = 500

    def route_change(route: ft.RouteChangeEvent):
        print(f'INFO:\t{page.client_ip} - "{route.data}"', end=' ')
        troute = ft.TemplateRoute(route.data)
        page.views.clear()
        page.on_resized = None
        if troute.match(HomeView.ROUTE):
            page.views.append(HomeView(page))
        elif troute.match(ImagesView.ROUTE):
            page.views.append(ImagesView(page))
        elif troute.match(SearchImagesView.ROUTE):
            page.views.append(SearchImagesView(page))
        elif troute.match(ImageView.ROUTE):
            page.views.append(ImageView(page, troute.image_id))
        elif troute.match(DeleteImagesView.ROUTE):
            page.views.append(DeleteImagesView(page))
        else:
            print(f'- REDIRECT TO "{HomeView.ROUTE}"', end=' ')
            page.views.append(HomeView(page))
        page.update()
        if len(page.views) > 0:
            print('200 OK')

    page.on_route_change = route_change
    page.go('/')

if __name__ == '__main__':
    os.makedirs(settings.TEMP_DIR, exist_ok=True)
    print(f'Start compose on {settings.FRONTEND_HOST}:{settings.FRONTEND_PORT}')
    ft.app(target=main, host=settings.FRONTEND_HOST, port=settings.FRONTEND_PORT, view=ft.AppView.WEB_BROWSER, upload_dir=settings.TEMP_DIR)