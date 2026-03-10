from pydantic_settings import BaseSettings 
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
ENV_PATH = BASE_DIR / '.env'

class Settings(BaseSettings):
    ALGORITHM: str = 'HS256'
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60*24*7
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 60*24*30

    SECRET_KEY: str
    DATABASE_URL: str
    ECHO: bool = False

    class Config:
        env_file = ENV_PATH
        env_file_encoding = 'utf-8'
        case_sensitive = True

settings = Settings()