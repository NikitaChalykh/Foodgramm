from django.urls import include, path
from .views import (get_token, delete_token, UserViewSet)
from rest_framework import routers

app_name = 'users'

router_users = routers.DefaultRouter()

router_users.register('users', UserViewSet)

urlpatterns = [
    path('users/', include(router_users.urls)),
    path('auth/token/login/', get_token, name='get_token'),
    path('auth/token/logout/', delete_token, name='delete_token')
]
