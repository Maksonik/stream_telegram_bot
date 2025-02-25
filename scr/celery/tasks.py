import asyncio
import datetime
import logging

from scr.celery.app import app
from scr.parser import ParserYouTube
from scr.telegram_bot import TelegramBot
from scr.types import DataVideo
from scr.utils import is_scheduled, get_time

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
    title_all_messages = list(map(lambda x: x.title, telegram.LIST_MESSAGES))
    if scheduled and data.title not in title_all_messages:
        notify_scheduled_youtube_channel_video(data=data)
    elif scheduled and get_time(data.time_scheduled_video) - datetime.timedelta(minutes=15) < datetime.datetime.now():
        notify_scheduled_youtube_channel_video(data=data, has_15_minutes_notice=True)
    elif not scheduled and data.title in title_all_messages:
        delete_notify_scheduled_youtube_channel_video(data=data)
    else:
        logging.info(f"Nothing's changed")


def notify_scheduled_youtube_channel_video(data: DataVideo, has_15_minutes_notice: bool = False) -> None:
    """
    Notify your Telegram channel of a scheduled video
    :param data: Data of video
    :param has_15_minutes_notice: 15 minutes' notice or not
    :return: None
    """
    logging.info(f"Send message: {data.title}, has_15_minutes_notice={has_15_minutes_notice}")
    asyncio.get_event_loop().run_until_complete(telegram.send_message(title=data.title,
                                                                      url=data.url_video,
                                                                      has_15_minutes_notice=has_15_minutes_notice))


def delete_notify_scheduled_youtube_channel_video(data: DataVideo) -> None:
    """
    Delete the notification of your Telegram channel about a scheduled video that has ended
    :param data: Data of video
    :return: None
    """
    logging.info(f"Delete message, title={data.title}")
    asyncio.get_event_loop().run_until_complete(telegram.delete_message())
