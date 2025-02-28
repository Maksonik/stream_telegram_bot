import datetime
import logging

import celery

from scr.apps.parser_client import ParserYouTube
from scr.apps.telegram_client import TelegramBot
from scr.celery.atask import AsyncTask
from scr.core.settings import get_settings
from scr.types import DataVideo, NotificationAction
from scr.utils import is_scheduled, get_time

settings = get_settings()
telegram = TelegramBot(settings=settings)
parser = ParserYouTube(settings=settings)


@celery.shared_task(name="sync_notify_about_first_youtube_video", base=AsyncTask)
async def sync_notify_about_first_youtube_video() -> None:
    """
    Checks if there is a notification of the first scheduled video on youtube channel,
     or remotely it if the stream has ended.
    :return: None
    """
    data = parser.get_information()
    title_all_messages = {x.title for x in telegram.LIST_MESSAGES}
    now = datetime.datetime.now()

    action = _determine_notification_action(data, title_all_messages, now)
    logging.info(f"Determined action '{action}' for video: {data.title}")

    match action:
        case NotificationAction.NOTIFY:
            await send_notification(data)
        case NotificationAction.NOTIFY_15:
            await send_notification(data, has_15_minutes_notice=True)
        case NotificationAction.DELETE:
            await delete_notification(data)
        case _:
            logging.info("Nothing's changed")


def _determine_notification_action(
    data: DataVideo, existing_titles: set[str], now: datetime.datetime
) -> NotificationAction:
    """
    Determines which action to perform
    :param data: Data of video
    :param existing_titles: List of title telegram posts
    :param now: time is now
    :return:
    """
    if data is None:
        return NotificationAction.NOTHING
    if not is_scheduled(data.time_scheduled_video):
        return NotificationAction.DELETE if existing_titles else NotificationAction.NOTHING
    if data.title not in existing_titles:
        return NotificationAction.NOTIFY

    scheduled_time = get_time(data.time_scheduled_video)
    if scheduled_time - datetime.timedelta(minutes=15) < now:
        return NotificationAction.NOTIFY_15

    return NotificationAction.NOTHING


async def send_notification(data: DataVideo, has_15_minutes_notice: bool = False) -> None:
    """
    Notify your Telegram channel of a scheduled video
    :param data: Data of video
    :param has_15_minutes_notice: 15 minutes' notice or not
    :return: None
    """
    logging.info(f"Send message: {data.title}, has_15_minutes_notice={has_15_minutes_notice}")
    await telegram.send_message(title=data.title, url=data.url_video, has_15_minutes_notice=has_15_minutes_notice)


async def delete_notification(data: DataVideo) -> None:
    """
    Delete the notification of your Telegram channel about a scheduled video that has ended
    :param data: Data of video
    :return: None
    """
    logging.info(f"Delete message, title={data.title}")
    await telegram.delete_message()
