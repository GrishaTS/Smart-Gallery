from flet import ControlEvent, Page, ThemeMode

def toggle_theme(e: ControlEvent) -> None:
    '''Переключает тему страницы между светлой и тёмной.'''
    e.page.theme_mode = (
        ThemeMode.DARK if e.page.theme_mode == ThemeMode.LIGHT else ThemeMode.LIGHT
    )
    e.page.update()
