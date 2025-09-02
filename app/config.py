import os

from dotenv import load_dotenv
from pydantic import AnyUrl, Field
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    APP_NAME: str = "Tournament API"
    DATABASE_URL: AnyUrl = Field(
        default=f"postgresql+asyncpg://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
    )

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()
