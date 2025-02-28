import logging
from typing import ClassVar

import telegram

from scr.core.settings import Settings
from scr.types import DataMessage


class TelegramBot:
    """Class for interacting with the telegram channel"""

    _instance: ClassVar = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(TelegramBot, cls).__new__(cls)
        return cls._instance

    def __init__(self, settings: Settings):
        self.LIST_MESSAGES: list[DataMessage] = []
        self.bot = telegram.Bot(settings.TELEGRAM_TOKEN)
        self.chat_id = settings.TELEGRAM_CHANNEL

    async def send_message(self, title, url, has_15_minutes_notice: bool = False) -> None:
        """
        Send a message about a scheduled stream video
        :param title: title of video
        :param url: url of video
        :param has_15_minutes_notice: 15 minutes' notice or not
        :return: None
        """
        logging.info(msg=f"Creating message, LIST_MESSAGES={self.LIST_MESSAGES}, TelegramBot={id(self)}")
        if not self.LIST_MESSAGES or not any(
            x.title == title and x.has_15_minutes_notice == has_15_minutes_notice for x in self.LIST_MESSAGES
        ):
            text = (
                f"I'm a bot, TEST VIDEO FOR 15 MINUTES! {url}"
                if has_15_minutes_notice
                else f"I'm a bot, TEST VIDEO! {url}"
            )
            message = await self.bot.send_message(chat_id=self.chat_id, text=text)
            self.LIST_MESSAGES.append(
                DataMessage(title=title, id=message.message_id, has_15_minutes_notice=has_15_minutes_notice)
            )
            logging.info(msg=f"Created message, id={message.message_id}, LIST_MESSAGES={self.LIST_MESSAGES}")

    async def delete_message(self) -> None:
        """
        Delete all messages about a scheduled streaming video that has passed
        :return: None
        """
        while self.LIST_MESSAGES:
            message = self.LIST_MESSAGES.pop()
            if message:
                logging.info(msg=f"Deleting message, id={message.id}")
                await self.bot.delete_message(chat_id=self.chat_id, message_id=message.id)
                logging.info(msg=f"Deleted message, id={message.id}")
