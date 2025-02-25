import datetime
import logging

import celery

from scr.apps.parser_client import ParserYouTube
from scr.apps.telegram_client import TelegramBot
from scr.celery.atask import AsyncTask
from scr.core.settings import get_settings
from scr.types import DataVideo
from scr.utils import is_scheduled, get_time

settings = get_settings()

telegram = TelegramBot(settings=settings)


@celery.shared_task(name="sync_notify_about_first_youtube_video", base=AsyncTask)
async def sync_notify_about_first_youtube_video() -> None:
    """
    Checks if there is a notification of the first scheduled video on youtube channel,
     or remotely it if the stream has ended.
    :return: None
    """
    data = ParserYouTube(settings=settings).get_information()
    scheduled = is_scheduled(data.time_scheduled_video)
    title_all_messages = {x.title for x in telegram.LIST_MESSAGES}

    if scheduled:
        if data.title not in title_all_messages:
            await notify_scheduled_youtube_channel_video(data=data)
        elif (
            scheduled and get_time(data.time_scheduled_video) - datetime.timedelta(minutes=15) < datetime.datetime.now()
        ):
            await notify_scheduled_youtube_channel_video(data=data, has_15_minutes_notice=True)
    else:
        if title_all_messages:
            await delete_notify_scheduled_youtube_channel_video(data=data)
        else:
            logging.info("Nothing's changed")


async def notify_scheduled_youtube_channel_video(data: DataVideo, has_15_minutes_notice: bool = False) -> None:
    """
    Notify your Telegram channel of a scheduled video
    :param data: Data of video
    :param has_15_minutes_notice: 15 minutes' notice or not
    :return: None
    """
    logging.info(f"Send message: {data.title}, has_15_minutes_notice={has_15_minutes_notice}")
    await telegram.send_message(title=data.title, url=data.url_video, has_15_minutes_notice=has_15_minutes_notice)


async def delete_notify_scheduled_youtube_channel_video(data: DataVideo) -> None:
    """
    Delete the notification of your Telegram channel about a scheduled video that has ended
    :param data: Data of video
    :return: None
    """
    logging.info(f"Delete message, title={data.title}")
    await telegram.delete_message()
