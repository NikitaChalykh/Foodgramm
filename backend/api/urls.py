from django.urls import include, path
from rest_framework import routers

from .views import (FavoriteViewSet, IngredientViewSet, RecipeViewSet,
                    ShoppingCartViewSet, TagViewSet)

app_name = 'api'

router_api = routers.DefaultRouter()

router_api.register('tags', TagViewSet)
router_api.register('ingredients', IngredientViewSet)
router_api.register('recipes', RecipeViewSet)

urlpatterns = [
    path('', include(router_api.urls)),
    path('recipes/<int:id>/shopping_cart/', ShoppingCartViewSet.as_view({
        'post': 'create',
        'delete': 'destroy'
    }), name='shopping_cart'),
    path('recipes/<int:id>/favorite/', FavoriteViewSet.as_view({
        'post': 'create',
        'delete': 'destroy'
    }), name='favorite')
]
