from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Formula(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='formulas'
    )
    title = models.CharField(
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

    class Meta:
        ordering = ['-pub_date']

    def __str__(self):
        return self.title[:15]


# class Comment(models.Model):
#     text = models.TextField(
#         verbose_name='Текст комментария',
#         help_text='Текст вашего комментария'
#     )
#     author = models.ForeignKey(
#         User,
#         on_delete=models.CASCADE,
#         related_name='comments'
#     )
#     post = models.ForeignKey(
#         Post,
#         on_delete=models.CASCADE,
#         related_name='comments'
#     )

#     def __str__(self):
#         return self.text[:15]
