import json
from typing import Any
from redis import Redis


class RedisStorage:
    """Class for working with Redis"""

    def __init__(self, host: str, port: int, key: str = "telegram_messages"):
        self.redis_client = Redis(host=host, port=port, decode_responses=True)
        self.key = key

    def add_message(self, message: dict) -> None:
        """
        Add a message to Redis
        :param message: message data
        :return: None
        """
        self.redis_client.lpush(self.key, json.dumps(message))

    def get_messages(self) -> list[dict[str, Any]]:
        """
        Get a list of messages from Redis
        :return: list of messages
        """
        messages = self.redis_client.lrange(self.key, 0, -1)
        return [json.loads(msg) for msg in messages] if messages else []

    def delete_message(self, message_id: int) -> None:
        """
        Deletes a message by ID
        :param message_id: ID of message from channel telegram
        :return: None
        """
        messages = self.get_messages()
        updated_messages = [msg for msg in messages if msg["id"] != message_id]
        self.redis_client.delete(self.key)
        for msg in updated_messages:
            self.redis_client.lpush(self.key, json.dumps(msg))

    def clear_all_messages(self) -> None:
        """
        Deletes all messages
        :return: None
        """
        self.redis_client.delete(self.key)
