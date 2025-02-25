import asyncio
import logging

from scr.celery.app import app
from scr.parser import ParserYouTube
from scr.telegram_bot import TelegramBot
from scr.types import DataVideo
from scr.utils import is_scheduled

telegram = TelegramBot()

@app.task
def sync_notify_about_first_youtube_video() -> None:
    """
    Checks if there is a notification of the first scheduled video on youtube channel,
     or remotely it if the stream has ended.
    :return: None
    """
    data = ParserYouTube.get_information()
    scheduled = is_scheduled(data.time_scheduled_video)
    if scheduled and data.title not in telegram.DICT_MESSAGES:
        notify_scheduled_youtube_channel_video(data=data)
    elif not scheduled and data.title in telegram.DICT_MESSAGES:
        delete_notify_scheduled_youtube_channel_video(data=data)
    else:
        logging.info(f"Nothing's changed")


def notify_scheduled_youtube_channel_video(data:DataVideo) -> None:
    """
    Notify your Telegram channel of a scheduled video
    :param data: Data of video
    :return: None
    """
    logging.info(f"Send message: {data.title}")
    asyncio.get_event_loop().run_until_complete(telegram.send_message(title=data.title, url=data.url_video))


def delete_notify_scheduled_youtube_channel_video(data:DataVideo) -> None:
    """
    Delete the notification of your Telegram channel about a scheduled video that has ended
    :param data: Data of video
    :return: None
    """
    logging.info(f"Delete message, title={data.title}")
    asyncio.get_event_loop().run_until_complete(telegram.delete_message())
