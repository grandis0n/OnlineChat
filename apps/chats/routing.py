from django.urls import path

from apps.chats import consumers

websocket_urlpatterns = [
    path('ws/<str:chat_name>/', consumers.ChatConsumer.as_asgi()),
]
