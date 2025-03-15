import os
import flet as ft
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import ClassVar
from functools import cached_property

class Settings(BaseSettings):
    FRONTEND_HOST: str
    FRONTEND_PORT: int
    BACKEND_HOST: str
    BACKEND_PORT: int
    MINIO_HOST: str
    MINIO_PORT: str
    MINIO_BUCKET_NAME: str
    TEMP_DIR : ClassVar[str] = '/frontend/temp'

    @cached_property
    def BACKEND_URL(self) -> str:
        return f"http://{self.BACKEND_HOST}:{self.BACKEND_PORT}"
    
    @cached_property
    def MINIO_BUCKET_URL(self):
        return f"http://{self.MINIO_HOST}:{self.MINIO_PORT}/{self.MINIO_BUCKET_NAME}"


settings = Settings()