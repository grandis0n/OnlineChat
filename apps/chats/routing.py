from django.urls import path

from apps.chats import consmers

websocket_urlpatterns = [
    path('ws/<str:chat_name>/', consmers.ChatConsumer.as_asgi()),
]
