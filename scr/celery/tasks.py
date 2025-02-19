import asyncio

from scr.celery.app import app
from scr.parser import ParserYouTube
from scr.telegram_bot import TelegramBot
from scr.utils import check_time_with_now


@app.task  # for tests
def add(x, y):
    return x + y

@app.task
def check_youtube_channel():
    telegram = TelegramBot()
    data = ParserYouTube().get_information()
    if check_time_with_now(data.time_scheduled_video):
        asyncio.run(
            telegram.send_message(title=data.title, url=data.url_video)
        )
    else:
        asyncio.run(telegram.delete_message())

