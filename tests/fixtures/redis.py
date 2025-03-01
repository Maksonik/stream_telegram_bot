import pytest
from redis import Redis
from scr.core.settings import get_settings


@pytest.fixture
def redis_client():
    """Create a synchronous connection to Redis and clear before each test"""
    settings = get_settings()
    redis = Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, decode_responses=True)
    redis.flushdb()

    yield redis

    redis.flushdb()
    redis.close()
