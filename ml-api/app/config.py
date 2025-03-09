import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    MEDIA_FOLDER: str
    BACKEND_HOST: str
    BACKEND_PORT: int
    FRONTEND_HOST: str
    FRONTEND_PORT: int
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int

    @property
    def FRONTEND_URL(self):
        return f'http://{self.FRONTEND_HOST}:{self.FRONTEND_PORT}'

    @property
    def BACKEND_URL(self):
        return f'http://{self.BACKEND_HOST}:{self.BACKEND_PORT}'
    
    @property
    def POSTGRES_URL(self):
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    @property
    def IMAGES_PATH(self):
        return os.path.join(self.MEDIA_FOLDER, 'images')

    @property
    def THUMBNAILS_PATH(self):
        return os.path.join(self.MEDIA_FOLDER, 'thumbnails')

    @property
    def EMBEDDINGS_PATH(self):
        return os.path.join(self.MEDIA_FOLDER, 'embeddings')

    @property
    def MEDIA_URL(self):
        return f'http://{self.BACKEND_HOST}:{self.BACKEND_PORT}/{self.MEDIA_FOLDER}'
    
    @property
    def IMAGES_URL(self):
        return os.path.join(self.MEDIA_URL, 'images')

    @property
    def THUMBNAILS_URL(self):
        return os.path.join(self.MEDIA_URL, 'thumbnails')

    @property
    def EMBEDDINGS_URL(self):
        return os.path.join(self.MEDIA_URL, 'embeddings')
    
settings = Settings()