from pydantic_settings import BaseSettings


class Settings(BaseSettings):

    APP_NAME: str = "Mai Nexus AI"

    APP_VERSION: str = "1.0.0"

    DEBUG: bool = True

    API_PREFIX: str = "/api/v1"

    SECRET_KEY: str = "CHANGE_THIS_SECRET_KEY"

    ALGORITHM: str = "HS256"

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    DATABASE_URL: str = (
        "postgresql://postgres:password@localhost/mai_nexus_ai"
    )

    CORS_ORIGINS: list[str] = [
        "http://localhost:3000",
        "http://127.0.0.1:3000"
    ]

    class Config:
        env_file = ".env"


settings = Settings()
