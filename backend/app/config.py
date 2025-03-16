from pydantic_settings import BaseSettings
from functools import cached_property
from typing import ClassVar

class Settings(BaseSettings):
    BACKEND_HOST: str
    BACKEND_PORT: int
    ML_API_HOST: str
    ML_API_PORT: int
    FRONTEND_HOST: str
    FRONTEND_PORT: int
    POSTGRES_DB: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    MINIO_ROOT_USER: str
    MINIO_ROOT_PASSWORD: str
    MINIO_HOST: str
    MINIO_PORT: int
    MINIO_BUCKET_NAME: str
    QDRANT_HOST: str
    QDRANT_PORT: int
    QDRANT_COLLECTION_NAME: str
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
    def MINIO_ENDPOINT(self):
        return f"{self.MINIO_HOST}:{self.MINIO_PORT}"

    @cached_property
    def MINIO_BUCKET_URL(self):
        return f"http://{self.MINIO_ENDPOINT}/{self.MINIO_BUCKET_NAME}"


settings = Settings()