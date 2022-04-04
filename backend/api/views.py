from io import StringIO

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
                          RecordRecipeSerializer, SmallRecipeSerializer,
                          TagSerializer, UserSerializer)
from .utils import (IngredientFilterBackend, PageLimitPaginator,
                    RecipeFilterBackend, delete_old_ingredients)


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
    filter_backends = (IngredientFilterBackend,)


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = FullRecipeSerializer
    pagination_class = PageLimitPaginator
    permission_classes = (RecipePermission,)
    filter_backends = (RecipeFilterBackend,)

    def get_serializer_class(self):
        if self.action == 'create' or self.action == 'partial_update':
            return RecordRecipeSerializer
        return FullRecipeSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        delete_old_ingredients(instance)
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
        myfile = StringIO()
        for position in shopping_list:
            position_ingredient = Ingredient.objects.get(
                pk=position['ingredient']
            )
            position_amount = position['average_amount']
            myfile.write(
                f' *  {position_ingredient.name.title()}'
                f' ({position_ingredient.measurement_unit})'
                f' - {position_amount}' + '\n'
            )
        response = HttpResponse(
            myfile.getvalue(),
            content_type='text'
        )
        response['Content-Disposition'] = (
            'attachment; filename="%s"' % 'shopping_list.txt'
        )
        return response


class ShoppingCartViewSet(viewsets.ViewSet):
    permission_classes = (permissions.IsAuthenticated,)

    def return_serialized_data(self, recipe, request):
        serializer = SmallRecipeSerializer(
            recipe, context={'request': request}
        )
        return Response(serializer.data, status.HTTP_201_CREATED)

    def create(self, request, id):
        recipe = get_object_or_404(Recipe, pk=id)
        if not recipe.shopping_list_recipes.filter(
            user=request.user
        ).exists():
            ShoppingList.objects.create(
                user=request.user,
                recipe=recipe
            )
            return self.return_serialized_data(recipe, request)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def check_and_delete_data(self, data):
        if data.exists():
            data.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, id):
        recipe = get_object_or_404(Recipe, pk=id)
        data = (
            recipe.shopping_list_recipes.filter(
                user=request.user
            )
        )
        return self.check_and_delete_data(data)


class FavoriteViewSet(ShoppingCartViewSet):

    def create(self, request, id):
        recipe = get_object_or_404(Recipe, pk=id)
        if not recipe.favorite_recipes.filter(
            user=request.user
        ).exists():
            FavoriteRecipe.objects.create(
                user=request.user,
                recipe=recipe
            )
            return self.return_serialized_data(recipe, request)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, id):
        recipe = get_object_or_404(Recipe, pk=id)
        data = (
            recipe.favorite_recipes.filter(user=request.user)
        )
        return self.check_and_delete_data(data)
