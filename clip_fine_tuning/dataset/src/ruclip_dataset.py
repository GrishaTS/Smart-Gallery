import sqlite3
import time
from tqdm import tqdm
import pandas as pd
from PIL import Image
from io import BytesIO
import requests
from torch.utils.data import Dataset
import os
import torch
import hashlib
from typing import List, Tuple
import random

rng = random.Random(42)


class ImageTextsRow:
    """
    Представляет одну запись из таблицы: включает в себя изображение и список текстов.

    Атрибуты:
        TIME_INTERVAL (int): Интервал ожидания между попытками скачивания.
        CACHE_DIR (str): Папка для кеширования изображений.
        DEVICE (str): CUDA или CPU.
        image (torch.Tensor): Преобразованное изображение.
        texts (List[str]): Список текстов, ассоциированных с изображением.
    """

    TIME_INTERVAL = 10
    CACHE_DIR = '.cache'
    DEVICE = 'cuda' if torch.cuda.is_available() else 'cpu'

    def __init__(self, row: pd.Series):
        """
        Инициализирует объект, скачивает и сохраняет изображение, обрабатывает список текстов.

        Args:
            row (pd.Series): Строка из DataFrame с колонкой image_url и несколькими текстами.
        """

        # получаю изображение и кэширую
        os.makedirs(self.CACHE_DIR, exist_ok=True)
        self.cache_path = self._get_cache_path(row['image_url'])
        if os.path.exists(self.cache_path):
            image = Image.open(self.cache_path).convert('RGB')
        else:
            image = self._download_and_cache_image(row['image_url'])
        texts = list(row[2:])
        rng.shuffle(texts)
        # Применяю процессинг для картинки и текстов
        self.image: torch.Tensor = ClipDataset.PROCESSOR(images=[image])['pixel_values'].squeeze(0).to(self.DEVICE)
        self.texts: List[torch.Tensor] = list(ClipDataset.PROCESSOR(text=texts)['input_ids'].to(self.DEVICE))

    def _get_cache_path(self, url: str) -> str:
        """
        Возвращает путь к кеш-файлу по URL изображения.

        Args:
            url (str): Ссылка на изображение.

        Returns:
            str: Путь к локальному кешированному изображению.
        """
        filename = hashlib.md5(url.encode()).hexdigest() + '.jpg'
        return os.path.join(self.CACHE_DIR, filename)

    def _download_and_cache_image(self, url: str) -> Image.Image:
        """
        Пытается скачать и сохранить изображение. Повторяет до 3 раз при ошибках.

        Args:
            url (str): Ссылка на изображение.

        Returns:
            Image.Image: Объект PIL.Image.

        Raises:
            RuntimeError: Если не удалось скачать изображение после 3 попыток.
        """
        for _ in range(3):
            try:
                response = requests.get(url, timeout=10)
                response.raise_for_status()
                image = Image.open(BytesIO(response.content)).convert('RGB')
                image.save(self.cache_path)
                return image
            except Exception:
                time.sleep(self.TIME_INTERVAL)
        raise RuntimeError(f"Ошибка при скачивании изображения: {url}")

    def __next__(self) -> Tuple[torch.Tensor, torch.Tensor]:
        """
        Возвращает пару (обработанное изображение, токенизированный текст).

        Returns:
            Tuple[torch.Tensor, torch.Tensor]: Тензоры изображения и текста.
        """
        self.texts.append(self.texts.pop(0))
        return self.image, self.texts[0]


class ClipDataset(Dataset):
    """
    Кастомный датасет для дообучения RuCLIP. Загружает пары (изображение, текст)
    из таблицы SQLite и преобразует в тензоры с помощью PROCESSOR.

    Атрибуты:
        PROCESSOR: Экземпляр процессора ruclip (должен быть задан извне).
        data (List[ImageTextsRow]): Список объектов, каждый из которых хранит изображение и тексты.
    """

    PROCESSOR = None  # должен быть установлен извне

    def __init__(self, db_path: str = 'dataset/clip.db', table_name='clip993'):
        """
        Загружает данные из таблицы table_name в базе данных и инициализирует кеш изображений.

        Args:
            db_path (str): Путь к SQLite-базе данных.
        """
        if not self.PROCESSOR:
            raise NotImplementedError('ClipDataset.PROCESSOR is None')
        conn = sqlite3.connect(db_path)
        self.data: List[ImageTextsRow] = []
        count = pd.read_sql_query(f'SELECT COUNT(*) FROM {table_name}', conn).iloc[0, 0]
        for idx, row in tqdm(pd.read_sql_query(f'SELECT * FROM {table_name}', conn).iterrows(), total=count):
            self.data.append(ImageTextsRow(row))


    def __len__(self) -> int:
        """
        Возвращает длину датасета.

        Returns:
            int: Общее количество пар (изображение, текст).
        """
        return len(self.data)

    def __getitem__(self, index: int) -> Tuple[torch.Tensor, torch.Tensor]:
        """
        Возвращает следующую пару (изображение, текст) по индексу.

        Args:
            index (int): Индекс элемента.

        Returns:
            Tuple[torch.Tensor, torch.Tensor]: Тензоры изображения и текста.
        """
        return next(self.data[index])
