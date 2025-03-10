import os
from pydantic_settings import BaseSettings
from functools import cached_property
from typing import ClassVar

class Settings(BaseSettings):
    BACKEND_HOST: str
    BACKEND_PORT: int
    ML_API_HOST: str
    ML_API_PORT: str
    FRONTEND_HOST: str
    FRONTEND_PORT: int
    MEDIA_FOLDER: str
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    CLIP_THRESHOLD: ClassVar[int] = 0.3

    @cached_property
    def FRONTEND_URL(self):
        return f'http://{self.FRONTEND_HOST}:{self.FRONTEND_PORT}'

    @cached_property
    def BACKEND_URL(self):
        return f'http://{self.BACKEND_HOST}:{self.BACKEND_PORT}'
    
    @cached_property
    def ML_API_URL(self):
        return f'http://{self.ML_API_HOST}:{self.ML_API_PORT}'
    
    @cached_property
    def POSTGRES_URL(self):
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    @cached_property
    def IMAGES_PATH(self):
        return os.path.join(self.MEDIA_FOLDER, 'images')

    @cached_property
    def THUMBNAILS_PATH(self):
        return os.path.join(self.MEDIA_FOLDER, 'thumbnails')

    @cached_property
    def EMBEDDINGS_PATH(self):
        return os.path.join(self.MEDIA_FOLDER, 'embeddings')


settings = Settings()