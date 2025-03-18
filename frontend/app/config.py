from functools import cached_property
from typing import ClassVar

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Класс конфигурации настроек приложения.
    """

    FRONTEND_HOST: str
    FRONTEND_PORT: int
    BACKEND_HOST: str
    BACKEND_PORT: int
    MINIO_HOST: str
    MINIO_PORT: str
    MINIO_BUCKET_NAME: str

    TEMP_DIR: ClassVar[str] = "/frontend/temp"

    @cached_property
    def BACKEND_URL(self) -> str:
        """
        Генерирует URL для бэкенда.

        :return: Строка с URL бэкенда.
        """
        return f"http://{self.BACKEND_HOST}:{self.BACKEND_PORT}"

    @cached_property
    def MINIO_BUCKET_URL(self) -> str:
        """
        Генерирует URL для MinIO bucket.

        :return: Строка с URL MinIO.
        """
        return f"http://{self.MINIO_HOST}:{self.MINIO_PORT}/{self.MINIO_BUCKET_NAME}"


settings = Settings()
