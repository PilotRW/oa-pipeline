from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str
    ALEMBIC_DATABASE_URL: str

    KEEPA_API_KEY: str | None = None
    USE_KEEPA_REAL_API: bool = False

    AUTH_ENABLED: bool = False
    AUTH_SESSION_SECRET: str = "dev-insecure-session-secret"
    AUTH_ISSUER: str | None = None
    AUTH_CLIENT_ID: str | None = None
    AUTH_CLIENT_SECRET: str | None = None
    AUTH_REDIRECT_URI: str | None = None
    AUTH_GROUPS_CLAIM: str = "groups"
    AUTH_DEV_USER: str = "dev@mirenelle.local"
    AUTH_DEV_ROLES: str = "owner"

    class Config:
        env_file = ".env"


settings = Settings()
