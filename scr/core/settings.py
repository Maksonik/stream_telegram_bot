import os
from dataclasses import dataclass
from dotenv import load_dotenv


@dataclass
class Settings:
    TELEGRAM_TOKEN: str = ""
    TELEGRAM_CHANNEL: str = ""
    YOUTUBE_CHANNEL_URL: str = ""
    REDIS_URL: str = ""


def get_settings() -> Settings:
    load_dotenv()
    return Settings(
        TELEGRAM_TOKEN=os.environ["TELEGRAM_TOKEN"],
        TELEGRAM_CHANNEL=os.environ["TELEGRAM_CHANNEL"],
        YOUTUBE_CHANNEL_URL=os.environ["YOUTUBE_CHANNEL_URL"],
        REDIS_URL=os.environ["REDIS_URL"],
    )
