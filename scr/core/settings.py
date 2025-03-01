import os
from dataclasses import dataclass
from dotenv import load_dotenv


@dataclass
class Settings:
    TELEGRAM_TOKEN: str = ""
    TELEGRAM_CHANNEL: str = ""
    YOUTUBE_CHANNEL_URL: str = ""
    REDIS_URL: str = "redis://localhost:6379"
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379


def get_settings() -> Settings:
    load_dotenv()
    return Settings(
        TELEGRAM_TOKEN=os.environ["TELEGRAM_TOKEN"],
        TELEGRAM_CHANNEL=os.environ["TELEGRAM_CHANNEL"],
        YOUTUBE_CHANNEL_URL=os.environ["YOUTUBE_CHANNEL_URL"],
        REDIS_URL=os.environ["REDIS_URL"],
        REDIS_HOST=os.environ["REDIS_HOST"],
        REDIS_PORT=int(os.environ["REDIS_PORT"]),
    )
