import os
import flet as ft
from pydantic_settings import BaseSettings
from dataclasses import dataclass

class Settings(BaseSettings):
    HOST: str = "0.0.0.0"
    PORT: int = 3000
    API_HOST: str = os.getenv("API_HOST", "backend")
    API_PORT: int = int(os.getenv("API_PORT", 8000))
    API_URL: str = f"http://{API_HOST}:{API_PORT}"
    TEMP_DIR : str = '/frontend/temp'

settings = Settings()
