import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'gallery.db')

IMAGES_DIR = os.path.join(BASE_DIR, 'media', 'images')
PREVIEW_IMAGES_DIR = os.path.join(BASE_DIR, 'media', 'preview')

os.makedirs(IMAGES_DIR, exist_ok=True)
os.makedirs(PREVIEW_IMAGES_DIR, exist_ok=True)
