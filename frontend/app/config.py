from pydantic_settings import BaseSettings, SettingsConfigDict
import flet as ft

DARK_THEME = ft.Theme(
    color_scheme=ft.ColorScheme(
        primary=ft.colors.INDIGO_400,
        on_primary=ft.colors.WHITE,
        primary_container=ft.colors.INDIGO_700,
        on_primary_container=ft.colors.INDIGO_50,
        secondary=ft.colors.TEAL_300,
        on_secondary=ft.colors.BLACK,
        background=ft.colors.GREY_900,
        on_background=ft.colors.GREY_100,
        surface=ft.colors.GREY_900,
        on_surface=ft.colors.GREY_100,
        error=ft.colors.RED_400,
        on_error=ft.colors.WHITE,
        surface_tint=ft.colors.INDIGO_400,
        shadow=ft.colors.BLACK54,
    ),
    font_family="Inter",
    use_material3=True,
)

class Settings(BaseSettings):
    HOST: str = 'localhost'
    PORT: int = 5137

    API_HOST: str = 'localhost'
    API_PORT: int = 8000

    @property
    def API_URL(self):
        return f'http://{self.API_HOST}:{self.API_PORT}'
    
    model_config = SettingsConfigDict(env_file='.env')


settings = Settings()
