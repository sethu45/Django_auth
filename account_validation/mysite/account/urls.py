from django.urls import path
from .views import registration_view, login_view, logout_view, index, UserDashboardView

urlpatterns = [
    path('', index, name='home'),
    path('register/', registration_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('dashboard/', UserDashboardView.as_view(), name='dashboard'),
]
