from pydantic_settings import BaseSettings
from functools import cached_property

class Settings(BaseSettings):
    ML_API_HOST: str
    ML_API_PORT: str
    ML_API_MODEL: str
    BACKEND_HOST: str
    BACKEND_PORT: int

    @cached_property
    def BACKEND_URL(self):
        return f'http://{self.BACKEND_HOST}:{self.BACKEND_PORT}'
    
settings = Settings()