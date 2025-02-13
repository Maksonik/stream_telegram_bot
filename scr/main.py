import asyncio
import logging
import os
import telegram
from dotenv import load_dotenv

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

LIST_MESSAGES = []


async def send_message(bot: telegram.Bot):
    message = await bot.send_message(
        chat_id=os.environ["CHANNEL"], text="I'm a bot, please talk to me!"
    )
    LIST_MESSAGES.append(message.message_id)


async def delete_message(bot: telegram.Bot) -> None:
    while LIST_MESSAGES:
        message_id = LIST_MESSAGES.pop()
        await bot.delete_message(
            chat_id=os.environ["CHANNEL"], message_id=message_id
        )


async def main(bot):
    await send_message(bot)
    await send_message(bot)
    await asyncio.sleep(3)
    await delete_message(bot)


if __name__ == "__main__":
    load_dotenv()
    bot = telegram.Bot(os.environ["TELEGRAM_TOKEN"])

    asyncio.run(main(bot))
