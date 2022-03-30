from django.contrib.auth.hashers import check_password
from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework import mixins, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from food.models import (AmountIngredient, FavoriteRecipe, Ingredient, Recipe,
                         ShoppingList, Tag)
from users.models import Follow, User

from .permissions import RecipePermission, UserPermission
from .serializers import (FollowSerializer, FullRecipeSerializer,
                          IngredientSerializer, PasswordSerializer,
                          SmallRecipeSerializer, TagSerializer, UserSerializer)
from .utils import PageLimitPaginator


class UserViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = PageLimitPaginator
    permission_classes = (UserPermission,)

    @action(
        detail=False,
        methods=['GET'],
        permission_classes=(permissions.IsAuthenticated,)
    )
    def me(self, request):
        serializer = UserSerializer(request.user, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        detail=False,
        methods=['POST'],
        permission_classes=(permissions.IsAuthenticated,)
    )
    def set_password(self, request):
        serializer = PasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        password = serializer.validated_data['current_password']
        new_password = serializer.validated_data['new_password']
        username = request.user.username
        user = get_object_or_404(
            self.get_queryset(),
            username=username
        )
        if check_password(password, user.password):
            user.set_password(new_password)
            user.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(
        detail=False,
        methods=['GET'],
        permission_classes=(permissions.IsAuthenticated,),
    )
    def subscriptions(self, request):
        queryset = self.get_queryset().filter(
            following__user=request.user
        ).order_by('pk')
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = FollowSerializer(
                page, many=True, context={'request': request}
            )
            return self.get_paginated_response(serializer.data)
        serializer = FollowSerializer(
            queryset, many=True, context={'request': request}
        )
        return Response(serializer.data, status=status.HTTP_200_OK)


class FollowViewSet(viewsets.ViewSet):
    permission_classes = (permissions.IsAuthenticated,)

    def create(self, request, user_id):
        follow_author = get_object_or_404(User, pk=user_id)
        if follow_author != request.user and (
            not request.user.follower.filter(author=follow_author).exists()
        ):
            Follow.objects.create(
                user=request.user,
                author=follow_author
            )
            serializer = FollowSerializer(
                follow_author, context={'request': request}
            )
            return Response(serializer.data, status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, user_id):
        follow_author = get_object_or_404(User, pk=user_id)
        data_follow = request.user.follower.filter(author=follow_author)
        if data_follow.exists():
            data_follow.delete()
            return Response(status.HTTP_204_NO_CONTENT)
        return Response(status.HTTP_400_BAD_REQUEST)


class TagViewSet(
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientViewSet(TagViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer

    def get_queryset(self):
        name = self.request.query_params.get('name')
        if name is not None:
            regular_name = '^' + name
            return Ingredient.objects.filter(
                name__regex=regular_name
            )
        return Ingredient.objects.all()


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = FullRecipeSerializer
    pagination_class = PageLimitPaginator
    permission_classes = (RecipePermission,)

    def get_queryset(self):
        is_favorited = self.request.query_params.get('is_favorited')
        is_in_shopping_cart = self.request.query_params.get(
            'is_in_shopping_cart'
        )
        recipes_author = self.request.query_params.get('author')
        recipes_tags = self.request.query_params.getlist('tags')
        review_queryset = Recipe.objects.all()
        if is_favorited == '1':
            review_queryset = review_queryset.filter(
                favorite_recipes__user=self.request.user
            )
        if is_in_shopping_cart == '1':
            review_queryset = review_queryset.filter(
                shopping_list_recipes__user=self.request.user
            )
        if recipes_author is not None:
            review_queryset = review_queryset.filter(
                author=recipes_author
            )
        if recipes_tags != []:
            regular_tags = '|'.join(recipes_tags)
            review_queryset = review_queryset.filter(
                tags__slug__regex=regular_tags
            )
        return review_queryset.distinct()

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        old_amount_ingredients = AmountIngredient.objects.filter(
            recipes=instance
        )
        old_amount_ingredients.delete()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=False,
        methods=['GET'],
        permission_classes=(permissions.IsAuthenticated,),
    )
    def download_shopping_cart(self, request):
        shopping_list = AmountIngredient.objects.filter(
            recipes__shopping_list_recipes__user=request.user
        )
        shopping_list = shopping_list.values('ingredient').annotate(
            average_amount=Sum('amount')
        )
        with open("shopping_list.txt", "w") as file:
            for position in shopping_list:
                position_ingredient = Ingredient.objects.get(
                    pk=position['ingredient']
                )
                position_amount = position['average_amount']
                file.write(
                    f' *  {position_ingredient.name.title()}'
                    f' ({position_ingredient.measurement_unit})'
                    f' - {position_amount}' + '\n'
                )
        file = open('shopping_list.txt')
        response = HttpResponse(file, content_type='text')
        response['Content-Disposition'] = (
            'attachment; filename="%s"' % 'shopping_list.txt'
        )
        return response


class ShoppingCartViewSet(viewsets.ViewSet):
    permission_classes = (permissions.IsAuthenticated,)

    def create(self, request, id):
        recipe_in_shopping_cart = get_object_or_404(Recipe, pk=id)
        if not recipe_in_shopping_cart.shopping_list_recipes.filter(
            user=request.user
        ).exists():
            ShoppingList.objects.create(
                user=request.user,
                recipe=recipe_in_shopping_cart
            )
            serializer = SmallRecipeSerializer(
                recipe_in_shopping_cart, context={'request': request}
            )
            return Response(serializer.data, status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, id):
        recipe_in_shopping_cart = get_object_or_404(Recipe, pk=id)
        data_shopping_list = (
            recipe_in_shopping_cart.shopping_list_recipes.filter(
                user=request.user
            )
        )
        if data_shopping_list.exists():
            data_shopping_list.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class FavoriteViewSet(viewsets.ViewSet):
    permission_classes = (permissions.IsAuthenticated,)

    def create(self, request, id):
        favorite_recipe = get_object_or_404(Recipe, pk=id)
        if not favorite_recipe.favorite_recipes.filter(
            user=request.user
        ).exists():
            FavoriteRecipe.objects.create(
                user=request.user,
                recipe=favorite_recipe
            )
            serializer = SmallRecipeSerializer(
                favorite_recipe, context={'request': request}
            )
            return Response(serializer.data, status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, id):
        favorite_recipe = get_object_or_404(Recipe, pk=id)
        data_favorite = (
            favorite_recipe.favorite_recipes.filter(
                user=request.user
            )
        )
        if data_favorite.exists():
            data_favorite.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_400_BAD_REQUEST)
