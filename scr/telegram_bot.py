import logging
import os

import telegram

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)


class TelegramBot:
    def __init__(self):
        self.LIST_MESSAGES = []
        self.bot = telegram.Bot(os.environ["TELEGRAM_TOKEN"])


    async def send_message(self) -> None:
        message = await self.bot.send_message(
            chat_id=os.environ["CHANNEL"], text="I'm a bot, please talk to me!"
        )
        self.LIST_MESSAGES.append(message.message_id)


    async def delete_message(self) -> None:
        while self.LIST_MESSAGES:
            message_id = self.LIST_MESSAGES.pop()
            await self.bot.delete_message(
                chat_id=os.environ["CHANNEL"], message_id=message_id
        )


