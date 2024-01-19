from apps.chats import providers as chat_providers
from apps.chats.models import Chat


def get_all_chats() -> list[Chat]:
    return chat_providers.get_all_chats()


def get_chat_by_slug(slug: str) -> Chat:
    return chat_providers.get_chat_by_slug(slug)
