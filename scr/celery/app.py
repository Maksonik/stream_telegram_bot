import asyncio

from celery import Celery
from dotenv import load_dotenv

from scr.parser import ParserYouTube
from scr.telegram_bot import TelegramBot
from scr.utils import check_time_with_now

load_dotenv()
app = Celery("task", broker="redis://localhost:6379/0")


app.conf.beat_schedule = {
     "run-me-every-ten-seconds": {
         "task": "scr.celery.app.check_youtube_channel",
         "schedule": 15
     }
}

telegram = TelegramBot()


@app.task
def check_youtube_channel():
    data = ParserYouTube().get_information()
    if check_time_with_now(data.time_scheduled_video):
        asyncio.run(telegram.send_message(title=data.title, url=data.url_video))
    else:
        asyncio.run(telegram.delete_message())
