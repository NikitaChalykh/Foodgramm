from django.urls import include, path
from rest_framework import routers
from users.views import UserViewSet

app_name = 'api'

router_api = routers.DefaultRouter()

router_api.register('users', UserViewSet)

urlpatterns = [
    path('', include(router_api.urls))
]
