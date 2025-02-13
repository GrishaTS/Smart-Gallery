import os
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DB_NAME: str = 'gallery'
    MEDIA_PATH: str = 'storage'
    HOST: str = 'localhost'
    PORT: int = 8000

    UI_HOST: str = 'localhost'
    UI_PORT: int = 5137

    @property
    def UI_URL(self):
        return f'http://{self.UI_HOST}:{self.UI_PORT}'

    @property
    def DATABASE_URL(self):
        return f'sqlite+aiosqlite:///{self.DB_NAME}.db'
    
    @property
    def IMAGES_PATH(self):
        return os.path.join(self.MEDIA_PATH, 'images')
    
    @property
    def THUMBNAILS_PATH(self):
        return os.path.join(self.MEDIA_PATH, 'thumbnails')
    
    @property
    def EMBEDDINGS_PATH(self):
        return os.path.join(self.MEDIA_PATH, 'embeddings')

    model_config = SettingsConfigDict(env_file='.env')

settings = Settings()
