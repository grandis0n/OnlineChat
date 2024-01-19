from django.contrib import admin

from apps.chats.models import Chat


@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    model = Chat
    list_display = ('name', 'slug')
    readonly_fields = ("slug",)
