from apps.chats.models import Chat


def get_all_chats() -> list[Chat]:
    return Chat.objects.all()


def get_chat_by_slug(slug: str) -> Chat:
    return Chat.objects.get(slug=slug)
