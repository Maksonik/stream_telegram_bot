import asyncio
import logging

from scr.celery.app import app
from scr.parser import ParserYouTube
from scr.telegram_bot import TelegramBot
from scr.utils import is_scheduled

telegram = TelegramBot()


@app.task
def check_youtube_channel() -> None:
    data = ParserYouTube.get_information()
    scheduled = is_scheduled(data.time_scheduled_video)

    if scheduled:
        logging.info(f"Send message: {telegram.DICT_MESSAGES}")
        asyncio.get_event_loop().run_until_complete(
            telegram.send_message(title=data.title, url=data.url_video)
        )
        return

    if not scheduled and telegram.DICT_MESSAGES:
        logging.info(f"Delete message, is_scheduled={scheduled}")
        asyncio.get_event_loop().run_until_complete(telegram.delete_message())
