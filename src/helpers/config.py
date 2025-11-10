from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):

    APP_NAME: str = "MyApp"
    APP_VERSION: str = "0.1.0"
    OPENAI_API_KEY: str

    FILE_ALLOWED_TYPES: list[str]
    FILE_MAX_SIZE: int = 10

    FILE_DEFAULT_CHUNK_SIZE: int
    class Config:
        env_file = ".env"


def get_settings() -> Settings:
    return Settings()