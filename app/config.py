import os

from dotenv import load_dotenv
from pydantic import AnyUrl, Field
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    APP_NAME: str = "Tournament API"
    DATABASE_URL: AnyUrl = Field(
        default=os.getenv('DB_URL')
    )

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()
