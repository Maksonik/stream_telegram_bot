import logging
import os
from typing import ClassVar

import telegram

class TelegramBot:
    _instance: ClassVar = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(TelegramBot, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        self.DICT_MESSAGES = {}
        self.bot = telegram.Bot(os.environ["TELEGRAM_TOKEN"])

    async def send_message(self, title, url) -> None:
        logging.log(level=logging.INFO, msg=f"Creating message, DICT_MESSAGES={self.DICT_MESSAGES}, TelegramBot={id(self)}")
        if title not in self.DICT_MESSAGES:
            message = await self.bot.send_message(
                chat_id=os.environ["CHANNEL"],
                text=f"I'm a bot, please talk to me! {url}",
            )
            self.DICT_MESSAGES[title] = message.message_id
            logging.log(level=logging.INFO, msg=f"Created message, id={message.message_id}, DICT_MESSAGES={self.DICT_MESSAGES}")

    async def delete_message(self) -> None:
        while self.DICT_MESSAGES:
            message = self.DICT_MESSAGES.popitem()
            if message:
                logging.log(level=logging.INFO, msg=f"Deleting message, id={message[-1]}")
                await self.bot.delete_message(
                    chat_id=os.environ["CHANNEL"], message_id=message[-1]
                )
                logging.log(level=logging.INFO, msg=f"Deleted message, id={message[-1]}")
