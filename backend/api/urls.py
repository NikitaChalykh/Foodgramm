from django.urls import include, path
from rest_framework import routers

from .views import IngredientViewSet, TagViewSet

app_name = 'api'

router_api = routers.DefaultRouter()

router_api.register('tags', TagViewSet)
router_api.register('ingredients', IngredientViewSet)

urlpatterns = [
    path('', include(router_api.urls))
]
