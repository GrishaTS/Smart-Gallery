import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DB_NAME: str = "gallery"
    MEDIA_FOLDER: str = "storage"
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    UI_HOST: str = "0.0.0.0"
    UI_PORT: int = 3000
    DOCKER_HOST: str = "backend"

    @property
    def UI_URL(self):
        return f"http://{self.UI_HOST}:{self.UI_PORT}"

    @property
    def API_URL(self):
        return f"http://{self.HOST}:{self.PORT}"
    
    @property
    def DATABASE_URL(self):
        return f"sqlite+aiosqlite:///{self.DB_NAME}.db"

    @property
    def IMAGES_PATH(self):
        return os.path.join(self.MEDIA_FOLDER, "images")

    @property
    def THUMBNAILS_PATH(self):
        return os.path.join(self.MEDIA_FOLDER, "thumbnails")

    @property
    def EMBEDDINGS_PATH(self):
        return os.path.join(self.MEDIA_FOLDER, "embeddings")

    @property
    def MEDIA_URL(self):
        return f'http://backend:{self.PORT}/storage'
    
    @property
    def IMAGES_URL(self):
        return os.path.join(self.MEDIA_URL, "images")

    @property
    def THUMBNAILS_URL(self):
        return os.path.join(self.MEDIA_URL, "thumbnails")

    @property
    def EMBEDDINGS_URL(self):
        return os.path.join(self.MEDIA_URL, "embeddings")


settings = Settings()