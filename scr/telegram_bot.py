import logging
import os

import telegram

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)


class TelegramBot:
    def __init__(self):
        self.DICT_MESSAGES = {}
        self.bot = telegram.Bot(os.environ["TELEGRAM_TOKEN"])

    async def send_message(self, title, url) -> None:
        if not self.DICT_MESSAGES.get(title, None):
            message = await self.bot.send_message(
                chat_id=os.environ["CHANNEL"],
                text=f"I'm a bot, please talk to me! {url}",
            )
            self.DICT_MESSAGES[title] = message.message_id

    async def delete_message(self) -> None:
        while self.DICT_MESSAGES:
            message = self.DICT_MESSAGES.popitem()
            if message:
                await self.bot.delete_message(
                    chat_id=os.environ["CHANNEL"], message_id=message[-1]
                )
