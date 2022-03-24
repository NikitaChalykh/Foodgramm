from django.urls import include, path
from rest_framework import routers
from users.views import UserViewSet, SubscribeViewSet

from .views import IngredientViewSet, TagViewSet

app_name = 'api'

router_api = routers.DefaultRouter()

router_api.register('users', UserViewSet)
router_api.register('tags', TagViewSet)
router_api.register('ingredients', IngredientViewSet)
router_api.register(
    r'^users/(?P<user_id>\d+)/subscribe',
    SubscribeViewSet,
    basename='subscribe')

urlpatterns = [
    path('', include(router_api.urls))
]
