import json
import logging

from channels.generic.websocket import AsyncWebsocketConsumer
from django.core.cache import cache
from django.utils import timezone

from services.redis import RedisService


class ChatConsumer(AsyncWebsocketConsumer):
    _MAX_MESSAGES_PER_MINUTE = 10
    _MESSAGE_CACHE_TIMEOUT = 1  # Timeout in seconds

    def __init__(self):
        super().__init__()
        self._logger = logging.getLogger(__name__)
        self._chat_name = ''
        self._chat_group_name = ''
        self.redis_service = RedisService()

    async def connect(self):
        # Get chat name from query string
        self._chat_name = self.scope['url_route']['kwargs']['chat_name']
        self._chat_group_name = f'chat_{self._chat_name}'

        self._logger.error(f'Connecting to {self._chat_group_name}')

        # Join chat group
        await self.channel_layer.group_add(
            self._chat_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        self._logger.error(f'Disconnecting from {self._chat_group_name}')
        await self.channel_layer.group_discard(
            self._chat_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        username = text_data_json['username']
        chat = text_data_json['chat']

        # Generate a cache key for the user's message rate limit
        cache_key = f'message_limit:{chat}:{username}'

        # Check if the user has reached the message limit within the time frame
        message_count = cache.get(cache_key, 0)
        current_time = timezone.now()
        last_message_time = cache.get(f'last_message_time:{chat}:{username}')

        if last_message_time and (current_time - last_message_time).seconds < self._MESSAGE_CACHE_TIMEOUT:
            # User sent a message too quickly, reject it
            self._logger.error('Rate limit exceeded. Message rejected.')
            return

        if message_count >= self._MAX_MESSAGES_PER_MINUTE:
            # User has exceeded the message limit, reject it
            self._logger.error('Rate limit exceeded. Message rejected.')
            return

        if message.strip():
            # Increment the message count and set the last message time
            cache.set(cache_key, message_count + 1, self._MESSAGE_CACHE_TIMEOUT)
            cache.set(f'last_message_time:{chat}:{username}', current_time, self._MESSAGE_CACHE_TIMEOUT)

            self._logger.error(f'Data received: {text_data_json}')

            # Store the message in Redis temporarily
            await self.redis_service.store_message_in_redis(chat_slug=chat, username=username, message=message)

            # Send message to chat group
            await self.channel_layer.group_send(
                self._chat_group_name,
                {
                    'type': 'chat_message',
                    'message': message,
                    'username': username,
                    'chat': chat,
                }
            )
        else:
            self._logger.error('Received an empty message')

    async def chat_message(self, event: dict):
        message = event['message']
        username = event['username']
        chat = event['chat']

        self._logger.error(f'Sending message to WebSocket: {event}')

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'username': username,
            'chat': chat,
        }))
