from rest_framework.pagination import PageNumberPagination


class PageLimitPaginator(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'limit'
    max_page_size = 10


def delete_old_ingredients(recipe):
    old_ingredients = recipe.ingredients.all()
    for old_ingredient in old_ingredients:
        if old_ingredient.recipes.count() == 1:
            old_ingredient.delete()
