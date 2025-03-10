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
    TEMP_DIR : ClassVar[str] = '/frontend/temp'

    @cached_property
    def BACKEND_URL(self) -> str:
        return f"http://{self.BACKEND_HOST}:{self.BACKEND_PORT}"

settings = Settings()