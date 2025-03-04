import logging

from pydantic import BaseSettings

from app.core.constants import LOG_FORMAT


class Settings(BaseSettings):
    app_title: str = 'QRKot'
    app_description: str = 'Благотворительный фонд поддержки котиков QRKot'
    database_url: str = 'sqlite+aiosqlite:///./fastapi.db'
    secret: str = 'secret'

    class Config:
        env_file = '.env'


settings = Settings()


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)
