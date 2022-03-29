from django.urls import include, path
from djoser.views import TokenCreateView, TokenDestroyView
from rest_framework import routers

from .views import (FavoriteViewSet, FollowViewSet, IngredientViewSet,
                    RecipeViewSet, ShoppingCartViewSet, TagViewSet,
                    UserViewSet)

app_name = 'api'

router_api = routers.DefaultRouter()

router_api.register('users', UserViewSet)
router_api.register('tags', TagViewSet)
router_api.register('ingredients', IngredientViewSet)
router_api.register('recipes', RecipeViewSet)

urlpatterns = [
    path('auth/token/login/', TokenCreateView.as_view(), name='token_login'),
    path(
        'auth/token/logout/', TokenDestroyView.as_view(), name='token_logout'
    ),
    path('', include(router_api.urls)),
    path('users/<int:user_id>/subscribe/', FollowViewSet.as_view({
        'post': 'create',
        'delete': 'destroy'
    }), name='subscribe'),
    path('recipes/<int:id>/shopping_cart/', ShoppingCartViewSet.as_view({
        'post': 'create',
        'delete': 'destroy'
    }), name='shopping_cart'),
    path('recipes/<int:id>/favorite/', FavoriteViewSet.as_view({
        'post': 'create',
        'delete': 'destroy'
    }), name='favorite')
]
