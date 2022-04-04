from rest_framework import filters
from rest_framework.pagination import PageNumberPagination


class PageLimitPaginator(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'limit'
    max_page_size = 10


class IngredientFilterBackend(filters.BaseFilterBackend):

    def filter_queryset(self, request, queryset, view):
        name = request.query_params.get('name')
        if name is not None:
            regular_name = '^' + name
            return queryset.filter(
                name__regex=regular_name
            )
        return queryset


class RecipeFilterBackend(filters.BaseFilterBackend):

    def filter_queryset(self, request, queryset, view):
        is_favorited = request.query_params.get('is_favorited')
        is_in_shopping_cart = request.query_params.get(
            'is_in_shopping_cart'
        )
        recipes_author = request.query_params.get('author')
        recipes_tags = request.query_params.getlist('tags')
        review_queryset = queryset
        if is_favorited == '1':
            review_queryset = review_queryset.filter(
                favorite_recipes__user=request.user
            )
        if is_in_shopping_cart == '1':
            review_queryset = review_queryset.filter(
                shopping_list_recipes__user=request.user
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


def delete_old_ingredients(recipe):
    old_ingredients = recipe.ingredients.all()
    for old_ingredient in old_ingredients:
        if old_ingredient.recipes.count() == 1:
            old_ingredient.delete()
