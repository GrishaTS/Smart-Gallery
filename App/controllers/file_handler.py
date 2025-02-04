import os
from config import IMAGES_DIR

def delete_selected_images(selected_images, images, page):
    for img in selected_images:
        image_path = os.path.join(IMAGES_DIR, img)
        if os.path.exists(image_path):
            os.remove(image_path)
            images.remove(img)
    selected_images.clear()
    page.update()

def delete_image(page, images, current_index):
    if not images:
        page.go("/")
        return

    if 0 <= current_index < len(images):
        image_to_delete = images[current_index]
        image_path = os.path.join(IMAGES_DIR, image_to_delete)

        if os.path.exists(image_path):
            os.remove(image_path)
            images.remove(image_to_delete)

    if not images:  # Если после удаления список пуст, возвращаем в главное меню
        page.go("/")
    else:
        # Если есть следующее изображение, идем к нему, иначе к последнему
        next_index = min(current_index, len(images) - 1)
        page.go(f"/image?img={images[next_index]}")
