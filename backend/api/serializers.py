from drf_extra_fields.fields import Base64ImageField
from food.models import AmountIngredient, Ingredient, Recipe, Tag
from rest_framework import serializers
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email', 'id', 'username', 'first_name',
            'last_name', 'is_subscribed'
        )

    def get_is_subscribed(self, obj):
        if self.context['request'].user.is_authenticated:
            return obj.following.filter(
                user=self.context['request'].user
            ).exists()
        return False

    def validate(self, data):
        if data.get('username') == 'me':
            raise serializers.ValidationError(
                'Username указан неверно!')
        return data

    def create(self, validated_data):
        return User.objects.create_user(
            **validated_data, password=self.initial_data['password']
        )


class FollowSerializer(UserSerializer):
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email', 'id', 'username', 'first_name',
            'last_name', 'is_subscribed', 'recipes', 'recipes_count'
        )

    def get_recipes(self, obj):
        recipes_limit = (
            self.context['request'].query_params.get('recipes_limit')
        )
        recipes = obj.recipes.all()
        if recipes_limit is not None:
            recipes_limit = int(recipes_limit)
            serializer = SmallRecipeSerializer(
                recipes[:recipes_limit], many=True
            )
        else:
            serializer = SmallRecipeSerializer(recipes, many=True)
        return serializer.data

    def get_recipes_count(self, obj):
        return obj.recipes.count()


class PasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(max_length=150)
    current_password = serializers.CharField(max_length=150)


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class AmountIngredientSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()
    measurement_unit = serializers.SerializerMethodField()

    class Meta:
        model = AmountIngredient
        fields = ('id', 'name', 'measurement_unit', 'amount')

    def get_id(self, obj):
        return obj.ingredient.id

    def get_name(self, obj):
        return obj.ingredient.name

    def get_measurement_unit(self, obj):
        return obj.ingredient.measurement_unit


class SmallRecipeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class FullRecipeSerializer(serializers.ModelSerializer):
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    tags = TagSerializer(read_only=True, many=True)
    author = UserSerializer(read_only=True)
    ingredients = AmountIngredientSerializer(read_only=True, many=True)
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = (
            'id', 'tags', 'author', 'ingredients',
            'is_favorited', 'is_in_shopping_cart', 'name',
            'image', 'text', 'cooking_time'
        )

    def get_is_favorited(self, obj):
        if (
            self.context['request'].user.is_authenticated
            and obj.favorite_recipes.filter(
                user=self.context['request'].user
            ).exists()
        ):
            return True
        return False

    def get_is_in_shopping_cart(self, obj):
        if (
            self.context['request'].user.is_authenticated
            and obj.shopping_list_recipes.filter(
                user=self.context['request'].user
            ).exists()
        ):
            return True
        return False

    def create(self, validated_data):
        author = self.context['request'].user
        ingredients = self.initial_data['ingredients']
        tags = self.initial_data['tags']

        queryset_tags = []
        for tag in tags:
            queryset_tags.append(Tag.objects.get(id=tag))

        queryset_amount_ingredients = []
        for new_ingredient in ingredients:
            ingredient = Ingredient.objects.get(id=new_ingredient['id'])
            amount_ingredient = AmountIngredient.objects.create(
                ingredient=ingredient,
                amount=new_ingredient['amount']
            )
            amount_ingredient.save()
            queryset_amount_ingredients.append(amount_ingredient)

        recipe = Recipe.objects.create(
            **validated_data,
            author=author
        )
        recipe.tags.set(queryset_tags)
        recipe.ingredients.set(queryset_amount_ingredients)
        return recipe

    def update(self, instance, validated_data):
        ingredients = self.initial_data['ingredients']
        tags = self.initial_data['tags']
        queryset_tags = []
        for tag in tags:
            queryset_tags.append(Tag.objects.get(id=tag))
        queryset_amount_ingredients = []
        old_amount_ingredients = AmountIngredient.objects.filter(
            recipes=instance
        )
        old_amount_ingredients.delete()
        for new_ingredient in ingredients:
            ingredient = Ingredient.objects.get(id=new_ingredient['id'])
            amount_ingredient = AmountIngredient.objects.create(
                ingredient=ingredient,
                amount=new_ingredient['amount']
            )
            amount_ingredient.save()
            queryset_amount_ingredients.append(amount_ingredient)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        instance.tags.set(queryset_tags)
        instance.ingredients.set(queryset_amount_ingredients)
        return instance
