import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'gallery.db')

IMAGES_DIR = os.path.join(BASE_DIR, 'media', 'images')
PREVIEW_DIR = os.path.join(BASE_DIR, 'media', 'preview')
EMBEDS_DIR = os.path.join(BASE_DIR, 'media', 'embeds')

os.makedirs(IMAGES_DIR, exist_ok=True)
os.makedirs(PREVIEW_DIR, exist_ok=True)
