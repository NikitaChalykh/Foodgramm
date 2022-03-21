from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Tag(models.Model):
    title = models.CharField(
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


class Ingredient(models.Model):
    author = models.ForeignKey(
        User,
        verbose_name='Автор рецепта',
        on_delete=models.CASCADE,
        related_name='formulas'
    )
    title = models.CharField(
        verbose_name='Название рецепта',
        max_length=200
    )


class Formula(models.Model):
    author = models.ForeignKey(
        User,
        verbose_name='Автор рецепта',
        on_delete=models.CASCADE,
        related_name='formulas'
    )
    title = models.CharField(
        verbose_name='Название рецепта',
        max_length=200
    )
    image = models.ImageField(
        verbose_name='Картинка рецепта',
        upload_to='formulas/',
        help_text='Загрузите сюда картинку вашего рецепта'
    )
    text = models.TextField(
        verbose_name='Текст рецепта',
        help_text='Текстовое описание рецепта'
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        verbose_name='Ингридиенты рецепта'
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name='Тэги рецепта'
    )
    time = models.DurationField(
        verbose_name='Время приготолвения рецепта',
    )

    class Meta:
        verbose_name = "Рецепт"
        verbose_name_plural = "Рецепты"

    def __str__(self):
        return self.title[:15]
