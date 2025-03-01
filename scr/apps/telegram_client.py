import logging
import random
from datetime import datetime
from typing import ClassVar

import telegram

from scr.apps.redis_storage import RedisStorage
from scr.constants import STREAM_CREATION_NOTIFICATION_LIST, STREAM_15_MINUTES_NOTIFICATION_LIST
from scr.core.settings import Settings


class TelegramBot:
    """Class for interacting with the telegram channel"""

    _instance: ClassVar = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(TelegramBot, cls).__new__(cls)
        return cls._instance

    def __init__(self, settings: Settings):
        self.storage: RedisStorage = RedisStorage(settings.REDIS_HOST, settings.REDIS_PORT)
        self.bot = telegram.Bot(settings.TELEGRAM_TOKEN)
        self.chat_id = settings.TELEGRAM_CHANNEL

    async def send_message(self, title: str, time: datetime, url: str, has_15_minutes_notice: bool = False) -> None:
        """
        Send a message about a scheduled stream video
        :param title: title of video
        :param time: Start time of a stream
        :param url: url of video
        :param has_15_minutes_notice: 15 minutes' notice or not
        :return: None
        """
        messages = self.storage.get_messages()
        logging.info(msg=f"Creating message, LIST_MESSAGES={messages}, TelegramBot={id(self)}")
        if not messages or not any(
            message["title"] == title and message["has_15_minutes_notice"] == has_15_minutes_notice
            for message in messages
        ):
            text = (
                random.choice(STREAM_15_MINUTES_NOTIFICATION_LIST)
                if has_15_minutes_notice
                else random.choice(STREAM_CREATION_NOTIFICATION_LIST)
            )
            text = text.format(time=time.strftime("%H:%M %d.%m.%Y"), url=f"https://www.youtube.com{url}")
            message = await self.bot.send_message(chat_id=self.chat_id, text=text)

            message_data = {"title": title, "id": message.message_id, "has_15_minutes_notice": has_15_minutes_notice}
            self.storage.add_message(message_data)
            logging.info(msg=f"Created message, id={message.message_id}, message_data={message_data}")

    async def delete_message(self) -> None:
        """
        Delete all messages about a scheduled streaming video that has passed
        :return: None
        """
        messages = self.storage.get_messages()
        for message in messages:
            logging.info(msg=f"Deleting message, id={message['id']}")
            await self.bot.delete_message(chat_id=self.chat_id, message_id=message["id"])
            self.storage.delete_message(message["id"])
            logging.info(msg=f"Deleted message, id={message['id']}")
