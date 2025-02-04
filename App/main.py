import flet as ft
from routes import setup_routes
from utils.database import init_db


def main(page: ft.Page):
    page.title = "Фотогалерея"
    page.theme_mode = "system"
    page.padding = 20
    page.window.min_width = 400
    page.window.min_height = 500

    setup_routes(page)


if __name__ == "__main__":
    init_db()
    ft.app(target=main)