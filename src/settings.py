from pathlib import Path
from pydantic_settings import BaseSettings

path = Path(__file__).resolve().parent
path = Path(path)


class Settings(BaseSettings):
    class Config:
        env_file = path.parent / '.env'
        env_file_encoding = 'utf-8'
        env_prefix = ''
        case_sensitive = False
        extra = 'ignore'

    bot_token: str


settings = Settings()
