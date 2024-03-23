from django.urls import path
from account.api.views import (
    registration_view,
    user_info,
    # admin_users_view,
    # normal_user_welcome_view,
)

from rest_framework.authtoken.views import obtain_auth_token

app_name = 'account'

urlpatterns = [
    path('register', registration_view, name="register"),
    # -> see accounts/api/views.py for response and url info
    path('login', obtain_auth_token, name="login"),
    path('user_info', user_info, name='user_info'),
]
