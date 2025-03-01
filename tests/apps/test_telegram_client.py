from datetime import datetime

import pytest

from scr.apps.telegram_client import TelegramBot
from scr.core.settings import get_settings


@pytest.mark.vcr(record_mode="once")
async def test_telegram_client(redis_client):
    telegram_bot = TelegramBot(settings=get_settings())
    await telegram_bot.send_message(title="Test message", url="test_url", time=datetime(2025, 2, 28, 12, 0))

    assert len(telegram_bot.storage.get_messages()) == 1

    await telegram_bot.delete_message()

    assert len(telegram_bot.storage.get_messages()) == 0
