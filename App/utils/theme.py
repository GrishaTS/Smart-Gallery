def toggle_theme(e):
    e.page.theme_mode = "dark" if e.page.theme_mode == "light" else "light"
    e.page.update()
