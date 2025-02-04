def on_text_change(e):
    e.page.search_button.disabled = not bool(e.page.search_field.value)
    e.page.update()
