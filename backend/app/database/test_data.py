from io import BytesIO

import httpx
from fastapi import UploadFile

from app.repository import Repository


HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"}


async def fill_test_data(count: int = 50) -> None:
    """Заполняет тестовыми изображениями, загружая их с Picsum и добавляя в репозиторий."""
    async with httpx.AsyncClient(
        verify=False, headers=HEADERS, follow_redirects=True
    ) as client:
        for i in range(count):
            file_link = "https://picsum.photos/1000"
            file_name = f"lorem_picsum_{i}.jpeg"

            response = await client.get(file_link, timeout=5)
            response.raise_for_status()

            file_bytes = response.content

            await Repository.add(
                UploadFile(file=BytesIO(file_bytes), filename=file_name)
            )
