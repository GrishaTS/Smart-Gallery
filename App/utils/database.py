import uuid
import os
import shutil
from PIL import Image as PILImage, ImageOps
import sqlite3
from config import DB_PATH, IMAGES_DIR, PREVIEW_IMAGES_DIR

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    os.makedirs('media/images', exist_ok=True)
    os.makedirs('media/images', exist_ok=True)
    os.makedirs('media/preview', exist_ok=True)
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS images (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            image_path TEXT NOT NULL,
            preview_path TEXT NOT NULL,
            date_create TEXT DEFAULT (strftime('%Y-%m-%d %H:%M:%f', 'now')),
            size INTEGER NOT NULL
        );
    ''')
    conn.commit()
    cur.close()
    conn.close()

def get_preview_list(sort='date_create', order='DESC'):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(f'SELECT id, preview_path, strftime("%d.%m.%Y %H:%M:%f", date_create), size FROM images ORDER BY {sort} {order};')
    images = cur.fetchall()
    cur.close()
    conn.close()
    return images

def get_image_list(sort='date_create', order='DESC'):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(f'SELECT id, image_path FROM images ORDER BY {sort} {order};')
    images = cur.fetchall()
    cur.close()
    conn.close()
    return images

def insert_image(image_path):
    file_ext = os.path.splitext(image_path)[-1].lower()
    unique_name = f'{uuid.uuid4()}{file_ext}'
    unique_preview_name = f'preview_{uuid.uuid4()}{file_ext}'
    
    dest_path = os.path.join(IMAGES_DIR, unique_name)
    preview_path = os.path.join(PREVIEW_IMAGES_DIR, unique_preview_name)
    
    shutil.copy(image_path, dest_path)
    
    with PILImage.open(image_path) as img:
        img = ImageOps.fit(img, (140, 140), method=0, bleed=0.0, centering=(0.5, 0.5))
        img.save(preview_path)
    
    size = os.path.getsize(dest_path)
    
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('''
        INSERT INTO images (image_path, preview_path, size)
        VALUES (?, ?, ?)
    ''', (dest_path, preview_path, size))
    conn.commit()
    cur.close()
    conn.close()

def get_image_by_id(image_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT image_path FROM images WHERE id = ?;', (image_id,))
    image = cur.fetchone()
    cur.close()
    conn.close()
    return image[0]

def delete_image(image_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT image_path, preview_path FROM images WHERE id = ?;', (image_id,))
    image = cur.fetchone()
    if image:
        if os.path.exists(image['image_path']):
            os.remove(image['image_path'])
        if os.path.exists(image['preview_path']):
            os.remove(image['preview_path'])
        cur.execute('DELETE FROM images WHERE id = ?;', (image_id,))
        conn.commit()
    cur.close()
    conn.close()

def delete_all_images():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT image_path, preview_path FROM images;')
    images = cur.fetchall()
    
    for image in images:
        if os.path.exists(image['image_path']):
            os.remove(image['image_path'])
        if os.path.exists(image['preview_path']):
            os.remove(image['preview_path'])
    
    cur.execute('DELETE FROM images;')
    conn.commit()
    cur.close()
    conn.close()


def get_adjacent_images(image_id, sort, order):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute(f'SELECT {sort} FROM images WHERE id = ?', (image_id,))
    current_value = cur.fetchone()

    if not current_value:
        cur.close()
        conn.close()
        return {'previous': None, 'next': None}

    current_value = current_value[0]

    if order.upper() == 'ASC':
        prev_condition = f'{sort} < ? ORDER BY {sort} DESC, id DESC'
        next_condition = f'{sort} > ? ORDER BY {sort} ASC, id ASC'
    else:
        prev_condition = f'{sort} > ? ORDER BY {sort} ASC, id ASC'
        next_condition = f'{sort} < ? ORDER BY {sort} DESC, id DESC'

    cur.execute(f'SELECT id FROM images WHERE {prev_condition} LIMIT 1;', (current_value,))
    prev_image = cur.fetchone()

    cur.execute(f'SELECT id FROM images WHERE {next_condition} LIMIT 1;', (current_value,))
    next_image = cur.fetchone()

    cur.close()
    conn.close()

    return {
        'previous': prev_image[0] if prev_image else None,
        'next': next_image[0] if next_image else None
    }