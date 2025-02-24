import asyncio
import logging

from scr.celery.app import app
from scr.parser import ParserYouTube
from scr.telegram_bot import TelegramBot
from scr.utils import is_scheduled


@app.task
def check_youtube_channel() -> None:
    telegram = TelegramBot()
    data = ParserYouTube.get_information()
    if data and is_scheduled(data.time_scheduled_video):
        logging.log(level=logging.INFO, msg="Send message")
        asyncio.run(
            telegram.send_message(title=data.title, url=data.url_video)
        )
    else:
        logging.log(level=logging.INFO, msg="Delete message")
        asyncio.run(telegram.delete_message())
