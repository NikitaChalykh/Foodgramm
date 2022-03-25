from django.contrib import admin

from .models import (AmountIngredient, FavoriteRecipe, Ingredient, Recipe,
                     ShoppingList, Tag)

admin.site.register(Tag)
admin.site.register(Ingredient)
admin.site.register(AmountIngredient)
admin.site.register(Recipe)
admin.site.register(FavoriteRecipe)
admin.site.register(ShoppingList)
