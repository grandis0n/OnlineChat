from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.views.generic import FormView

from apps.accounts.forms import SignUpForm


class CustomLoginView(LoginView):
    template_name = 'login.html'

    def form_invalid(self, form):
        messages.error(self.request, 'Invalid username or password')
        return super(CustomLoginView, self).form_invalid(form)


class SignUpView(FormView):
    template_name = 'signup.html'
    form_class = SignUpForm
    success_url = '/'

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super(SignUpView, self).form_valid(form)
