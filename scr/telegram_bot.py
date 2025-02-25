import logging
import os
from typing import ClassVar

import telegram

from scr.types import DataMessage


class TelegramBot:
    """Class for interacting with the telegram channel"""

    _instance: ClassVar = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(TelegramBot, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        self.LIST_MESSAGES: list[DataMessage] = []
        self.bot = telegram.Bot(os.environ["TELEGRAM_TOKEN"])

    async def send_message(self, title, url) -> None:
        """
        Send a message about a scheduled stream video
        :param title: title of video
        :param url: url of video
        :return: None
        """
        logging.info(msg=f"Creating message, DICT_MESSAGES={self.LIST_MESSAGES}, TelegramBot={id(self)}")
        if title not in self.LIST_MESSAGES:
            message = await self.bot.send_message(
                chat_id=os.environ["CHANNEL"],
                text=f"I'm a bot, please talk to me! {url}",
            )
            self.LIST_MESSAGES.append(DataMessage(title=title, id=message.message_id))
            logging.info(msg=f"Created message, id={message.message_id}, DICT_MESSAGES={self.LIST_MESSAGES}")

    async def delete_message(self) -> None:
        """
        Delete all messages about a scheduled streaming video that has passed
        :return: None
        """
        while self.LIST_MESSAGES:
            message = self.LIST_MESSAGES.pop()
            if message:
                logging.info(msg=f"Deleting message, id={message.id}")
                await self.bot.delete_message(chat_id=os.environ["CHANNEL"], message_id=message.id)
                logging.info(msg=f"Deleted message, id={message.id}")
