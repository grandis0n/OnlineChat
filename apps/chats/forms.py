from django import forms

from apps.chats.models import Chat


class ChatCreateForm(forms.ModelForm):
    class Meta:
        model = Chat
        fields = (
            'name',
        )
