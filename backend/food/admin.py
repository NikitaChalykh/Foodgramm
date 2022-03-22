from django.contrib import admin

from .models import AmountIngredient, Formula, Ingredient, Tag

admin.site.register(Tag)
admin.site.register(Ingredient)
admin.site.register(AmountIngredient)
admin.site.register(Formula)
