import os
from dataclasses import dataclass
from dotenv import load_dotenv


@dataclass
class Settings:
    TELEGRAM_TOKEN: str = ""
    CHANNEL: str = ""
    YOUTUBE_CHANNEL_URL: str = ""
    REDIS_URL: str = ""


def get_settings() -> Settings:
    load_dotenv()
    return Settings(
        TELEGRAM_TOKEN=os.environ["TELEGRAM_TOKEN"],
        CHANNEL=os.environ["CHANNEL"],
        YOUTUBE_CHANNEL_URL=os.environ["YOUTUBE_CHANNEL_URL"],
        REDIS_URL=os.environ["REDIS_URL"],
    )
