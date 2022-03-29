# Generated by Django 2.2.16 on 2022-03-28 08:58

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('food', '0002_auto_20220327_1607'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='amountingredient',
            options={'ordering': ['ingredient'], 'verbose_name': 'Ингредиент в рецептах с количеством', 'verbose_name_plural': 'Ингредиенты в рецептах с количеством'},
        ),
        migrations.AlterModelOptions(
            name='ingredient',
            options={'ordering': ['name'], 'verbose_name': 'Ингредиент', 'verbose_name_plural': 'Ингредиенты'},
        ),
        migrations.AlterField(
            model_name='favoriterecipe',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favorite_recipes', to=settings.AUTH_USER_MODEL, verbose_name='Повар'),
        ),
        migrations.AlterField(
            model_name='shoppinglist',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shopping_list_recipes', to=settings.AUTH_USER_MODEL, verbose_name='Покупатель'),
        ),
        migrations.AlterUniqueTogether(
            name='amountingredient',
            unique_together={('ingredient', 'amount')},
        ),
    ]