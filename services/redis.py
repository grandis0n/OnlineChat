import json

import redis

from config.settings.base import REDIS_HOST, REDIS_PORT


class RedisService:
    _HOST = REDIS_HOST
    _PORT = REDIS_PORT

    def __init__(self):
        self.redis_client = redis.Redis(host=self._HOST, port=self._PORT, db=0)

    async def store_message_in_redis(self, chat_slug: str, message: str, username: str):
        # Create a message object with sender and text
        message_data = {
            'username': username,
            'message': message,
        }

        # Store the message in Redis
        self.redis_client.lpush(f'chat:{chat_slug}', json.dumps(message_data))

    def get_chat_messages(self, chat_slug: str) -> list[dict]:
        # Retrieve messages from Redis and parse them as JSON
        redis_messages = self.redis_client.lrange(f'chat:{chat_slug}', 0, -1)
        chat_messages = [json.loads(redis_message.decode('utf-8')) for redis_message in reversed(redis_messages)]
        return chat_messages
