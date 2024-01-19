from django.urls import path

from apps.chats.views import ChatListTemplate, ChatTemplate

app_name = 'chats'

urlpatterns = [
    path('', ChatListTemplate.as_view(), name='chats_list'),
    path('<slug:slug>/', ChatTemplate.as_view(), name='chat'),
]
