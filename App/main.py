import flet as ft
from routes import setup_routes
from utils.database import init_db


def main(page: ft.Page) -> None:
    'Инициализирует приложение Фотогалерея и настраивает маршруты.'
    page.title = 'Smart Gallery'
    page.theme_mode = 'system'
    page.padding = 20
    page.window_min_width = 400
    page.window_min_height = 500

    setup_routes(page)


if __name__ == '__main__':
    init_db()
    ft.app(target=main)
