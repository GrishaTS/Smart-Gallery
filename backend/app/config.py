import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import ClassVar


import os
print("ENV VARIABLES IN CONTAINER:")
for key in ["DB_NAME", "MEDIA_FOLDER", "BACKEND_HOST", "BACKEND_PORT", "FRONTEND_HOST", "FRONTEND_PORT"]:
    print(f"{key}={os.getenv(key)}")



class Settings(BaseSettings):
    DB_NAME: str
    MEDIA_FOLDER: str
    BACKEND_HOST: str
    BACKEND_PORT: int
    FRONTEND_HOST: str
    FRONTEND_PORT: int

    @property
    def FRONTEND_URL(self):
        return f'http://{self.FRONTEND_HOST}:{self.FRONTEND_PORT}'

    @property
    def BACKEND_URL(self):
        return f'http://{self.BACKEND_HOST}:{self.BACKEND_PORT}'
    
    @property
    def DATABASE_URL(self):
        return f'sqlite+aiosqlite:///{self.DB_NAME}.db'

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