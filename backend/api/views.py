from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework import mixins, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from food.models import (AmountIngredient, FavoriteRecipe, Ingredient, Recipe,
                         ShoppingList, Tag)

from .serializers import (FullRecipeSerializer, IngredientSerializer,
                          ReadFullRecipeSerializer, RecipeSerializer,
                          TagSerializer)


class TagViewSet(
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientViewSet(
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    search_fields = ('^name',)


class RecipeViewSet(viewsets.ModelViewSet):
    # доработать вьюсет рецептов
    queryset = Recipe.objects.all()
    serializer_class = ReadFullRecipeSerializer

    def get_serializer_class(self):
        if self.action == 'create':
            return FullRecipeSerializer
        return ReadFullRecipeSerializer

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
            serializer = RecipeSerializer(
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
            serializer = RecipeSerializer(
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
