import flet as ft
from config import DARK_THEME, settings
from views.images_view import ImagesView
from views.image_view import ImageView
from views.delete_images_view import DeleteImagesView
from views.search_images_view import SearchImagesView

def main(page: ft.Page):
    page.title = "Умная галерея"
    page.theme_mode = DARK_THEME
    page.padding = 20
    page.window.min_width = 400
    page.window.min_height = 500

    def route_change(route):
        page.views.clear()
        if page.route == "/":
            page.views.append(ImagesView(page))
        elif page.route == "/image":
            page.views.append(ImageView(page))
        elif page.route == "/delete":
            page.views.append(DeleteImagesView(page))
        elif page.route == "/search":
            page.views.append(SearchImagesView(page))
        page.update()

    page.on_route_change = route_change
    page.go("/")

if __name__ == "__main__":
    ft.app(target=main, host=settings.HOST, port=settings.PORT, view=None)