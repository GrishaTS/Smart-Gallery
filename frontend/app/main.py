import os
import flet as ft
from config import settings
from views import (
    HomeView,
    ImagesView,
    SearchImagesView,
    DeleteImagesView
)

def main(page: ft.Page):
    page.title = 'Умная галерея'
    page.theme_mode = 'system'
    page.padding = 20
    page.window.min_width = 400
    page.window.min_height = 500

    def route_change(route: ft.RouteChangeEvent):
        troute = ft.TemplateRoute(route.data)
        page.views.clear()
        if troute.match(HomeView.ROUTE):
            page.views.append(HomeView(page))
        elif troute.match(ImagesView.ROUTE):
            page.views.append(ImagesView(page))
        elif troute.match(SearchImagesView.ROUTE):
            page.views.append(SearchImagesView(page))
        # elif troute.match(ImageView.ROUTE):
        #     page.views.append(ImageView(page, troute.image_id))
        elif troute.match(DeleteImagesView.ROUTE):
            page.views.append(DeleteImagesView(page))
        else:
            page.views.append(HomeView(page))
        page.update()

    page.on_route_change = route_change
    page.go('/')

if __name__ == '__main__':
    os.makedirs(settings.TEMP_DIR, exist_ok=True)
    ft.app(target=main, host=settings.HOST, port=settings.PORT, view=ft.AppView.WEB_BROWSER, upload_dir=settings.TEMP_DIR)