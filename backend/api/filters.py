from rest_framework import filters


class IngredientFilterBackend(filters.BaseFilterBackend):

    def filter_queryset(self, request, queryset, view):
        name = request.query_params.get('name')
        if name is not None:
            begining_regular_name = '^' + name
            begining_regular_queryset = queryset.filter(
                name__regex=begining_regular_name
            )
            end_regular_name = name + '$'
            end_regular_queryset = queryset.filter(
                name__regex=end_regular_name
            )
            queryset = begining_regular_queryset | end_regular_queryset
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
        if recipes_tags:
            regular_tags = '|'.join(recipes_tags)
            review_queryset = review_queryset.filter(
                tags__slug__regex=regular_tags
            )
        return review_queryset.distinct()
