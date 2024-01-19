from django.contrib.auth import views as auth_views
from django.urls import path

from apps.accounts.views import SignUpView, CustomLoginView
# from apps.accounts.views import CustomLoginView

app_name = 'accounts'

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
