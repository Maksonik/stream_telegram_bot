import asyncio
from typing import Generator, Any

import pytest

from scr.core.settings import Settings, get_settings


@pytest.fixture(scope="session")
def event_loop_session() -> Generator[asyncio.AbstractEventLoop, Any, None]:
    """Single event loop for a test session.
    Otherwise, pytest will run each in a separate loop.
    """
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
def settings() -> Settings:
    return get_settings()
