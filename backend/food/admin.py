from django.contrib import admin

from .models import (AmountIngredient, FavoriteRecipe, Ingredient, Recipe,
                     ShoppingList, Tag)


class RecipeAdmin(admin.ModelAdmin):
    readonly_fields = ('добавлен_в_избранное',)
    list_display = (
        'name',
        'author'
    )
    list_filter = ('name', 'author', 'tags')
    search_fields = ('name',)
    empty_value_display = '-пусто-'

    def добавлен_в_избранное(self, instance):
        return instance.favorite_recipes.count()


class IngredientAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'measurement_unit'
    )
    list_filter = ('name',)
    search_fields = ('name',)
    empty_value_display = '-пусто-'


class AmountIngredientAdmin(admin.ModelAdmin):
    list_display = (
        'ingredient',
        'amount'
    )
    list_filter = ('ingredient', 'amount')
    search_fields = ('ingredient',)
    empty_value_display = '-пусто-'


class TagAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'color',
        'slug'
    )
    list_filter = ('name', 'color', 'slug')
    search_fields = ('name',)
    empty_value_display = '-пусто-'


class ShoppingListAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'recipe'
    )
    list_filter = ('user', 'recipe')
    search_fields = ('user',)
    empty_value_display = '-пусто-'


class FavoriteAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'recipe'
    )
    list_filter = ('user', 'recipe')
    search_fields = ('user',)
    empty_value_display = '-пусто-'


admin.site.register(Tag, TagAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(AmountIngredient, AmountIngredientAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(FavoriteRecipe, FavoriteAdmin)
admin.site.register(ShoppingList, ShoppingListAdmin)
