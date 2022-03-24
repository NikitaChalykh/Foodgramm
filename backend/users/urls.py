from django.urls import include, path
from djoser.views import TokenCreateView, TokenDestroyView
from rest_framework import routers

from .views import SubscribeViewSet, UserViewSet

app_name = 'users'

router_users = routers.DefaultRouter()

router_users.register('users', UserViewSet)

urlpatterns = [
    path('', include(router_users.urls)),
    path('users/<int:user_id>/subscribe', SubscribeViewSet.as_view({
        'post': 'create',
        'delete': 'destroy'
    })),
    path('token/login/', TokenCreateView.as_view(), name='token_login'),
    path('token/logout/', TokenDestroyView.as_view(), name='token_logout')
]
