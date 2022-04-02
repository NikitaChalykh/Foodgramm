from rest_framework.pagination import PageNumberPagination


class PageLimitPaginator(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'limit'
    max_page_size = 10


def delete_ingredients_in_recipe(recipe):
    ingredients = recipe.ingredients.all()
    for ingredient in ingredients:
        if ingredient.recipes.count() == 1:
            ingredient.delete()
