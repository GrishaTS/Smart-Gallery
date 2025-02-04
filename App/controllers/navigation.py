def navigate_image(page, direction):
    images = page.images
    current_image_index = (page.current_image_index + direction) % len(images)
    page.current_image_index = current_image_index
    page.show_image_view(images[current_image_index])
