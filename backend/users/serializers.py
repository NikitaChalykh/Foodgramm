from rest_framework import serializers

from api.serializers import RecipeSerializer
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
        if (self.context['request'].user.is_authenticated):
            return obj.following.filter(
                user=self.context['request'].user
            ).exists()
        return False

    def validate(self, data):
        if data.get('username') == 'me':
            raise serializers.ValidationError(
                'Username указан неверно!')
        return data


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
        queryset = obj.recipes.all()
        if recipes_limit is not None:
            recipes_limit = int(recipes_limit)
            serializer = RecipeSerializer(queryset[:recipes_limit], many=True)
        else:
            serializer = RecipeSerializer(queryset, many=True)
        return serializer.data

    def get_recipes_count(self, obj):
        return obj.recipes.count()


class SetPasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(max_length=150)
    current_password = serializers.CharField(max_length=150)
