from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Tag(models.Model):
    name = models.CharField(
        verbose_name='Название тега',
        max_length=50,
        unique=True
    )
    color = models.CharField(
        verbose_name='Цветовой HEX-код тега',
        max_length=100,
        unique=True
    )
    slug = models.SlugField(
        unique=True,
        verbose_name='Слаг тега'
    )

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"

    def __str__(self):
        return self.name[:15]


class Ingredient(models.Model):
    name = models.CharField(
        verbose_name='Название ингридиента',
        max_length=200
    )
    measurement_unit = models.CharField(
        verbose_name='Единицы измерения ингридиента',
        max_length=50
    )

    class Meta:
        verbose_name = "Ингридиент"
        verbose_name_plural = "Ингридиенты"

    def __str__(self):
        return self.name[:15]


class AmountIngredient(models.Model):
    ingredient = models.ForeignKey(
        Ingredient,
        verbose_name='Название ингридиента рецепта',
        on_delete=models.CASCADE
    )
    amount = models.FloatField(
        verbose_name='Колличество',
    )

    class Meta:
        verbose_name = "Ингридиент в рецепте"
        verbose_name_plural = "Ингридиенты в рецепте"

    def __str__(self):
        return self.ingredient.title[:15]


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        verbose_name='Автор рецепта',
        on_delete=models.CASCADE,
        related_name='recipes'
    )
    name = models.CharField(
        verbose_name='Название рецепта',
        max_length=200
    )
    image = models.ImageField(
        verbose_name='Картинка рецепта',
        upload_to='recipes/',
        help_text='Загрузите сюда картинку вашего рецепта'
    )
    text = models.TextField(
        verbose_name='Текст рецепта',
        help_text='Текстовое описание рецепта'
    )
    ingredients = models.ManyToManyField(
        AmountIngredient,
        verbose_name='Ингридиенты рецепта'
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name='Тэги рецепта'
    )
    cooking_time = models.IntegerField(
        verbose_name='Время приготовления рецепта',
    )

    class Meta:
        verbose_name = "Рецепт"
        verbose_name_plural = "Рецепты"

    def __str__(self):
        return self.title[:15]


class FavoriteRecipe(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='cook',
        verbose_name='Пользователь'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorite_recipes',
        verbose_name='Избранный рецепт'
    )

    class Meta:
        verbose_name = "Избранный рецепт"
        verbose_name_plural = "Избранные рецепты"

    def __str__(self):
        return self.user.username[:15]


class ShoppingList(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='buyer',
        verbose_name='Пользователь'
    )
    ingridient = models.ForeignKey(
        AmountIngredient,
        on_delete=models.CASCADE,
        related_name='favorite_recipes',
        verbose_name='Ингридиент для покупки'
    )

    class Meta:
        verbose_name = "Список покупок"
        verbose_name_plural = "Список покупок"

    def __str__(self):
        return self.user.username[:15]
