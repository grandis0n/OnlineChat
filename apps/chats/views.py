from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.cache import cache
from django.views.generic import TemplateView, FormView

from apps.chats import services as chat_services
from apps.chats.forms import ChatCreateForm
from apps.chats.models import Chat
from services.redis import RedisService


class ChatListTemplate(LoginRequiredMixin, FormView):
    template_name = 'chats.html'
    form_class = ChatCreateForm
    extra_context = {'chats': chat_services.get_all_chats()}
    success_url = '/'

    def form_valid(self, form):
        instance: Chat = form.save()
        # redirect to new chat page
        self.success_url += instance.slug
        messages.success(self.request, 'Chat created')
        return super(ChatListTemplate, self).form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Chat name already exists')
        return super(ChatListTemplate, self).form_invalid(form)


class ChatTemplate(LoginRequiredMixin, TemplateView):
    template_name = 'chat.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        slug = self.kwargs['slug']
        context['chat'] = chat_services.get_chat_by_slug(slug=slug)

        # Retrieve chat messages from Redis
        chat_messages = RedisService().get_chat_messages(chat_slug=slug)
        context['chat_messages'] = chat_messages
        return context
