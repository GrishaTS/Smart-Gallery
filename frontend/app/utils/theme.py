import flet as ft

def toggle_theme(e: ft.ControlEvent):
    e.page.theme_mode = 'dark' if e.page.theme_mode == 'light' else 'light'
    e.page.update()
