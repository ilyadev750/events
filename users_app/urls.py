from django.urls import path
from .views import register_user, user_login, user_logout, user_refresh_token


urlpatterns = [
    path('register/', register_user, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('user-refresh-token/', user_refresh_token, name='user-refresh-token')
]
