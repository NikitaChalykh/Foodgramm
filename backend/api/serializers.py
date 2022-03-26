from rest_framework import serializers

from food.models import Ingredient, Recipe, Tag


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class RecipeSerializer(serializers.ModelSerializer):
    # настрой все поля сериализатора (картинки и все такое)

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')