from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    HOST: str = 'localhost'
    PORT: int = 8000

    @property
    def API_URL(self):
        return f'http://{self.HOST}:{self.PORT}'
    model_config = SettingsConfigDict(env_file='.env')


settings = Settings()
