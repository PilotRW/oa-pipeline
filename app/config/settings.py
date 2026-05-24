from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str
    ALEMBIC_DATABASE_URL: str

    KEEPA_API_KEY: str | None = None
    USE_KEEPA_REAL_API: bool = False

    class Config:
        env_file = ".env"


settings = Settings()