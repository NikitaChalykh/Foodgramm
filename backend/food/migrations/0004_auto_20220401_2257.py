# Generated by Django 2.2.16 on 2022-04-01 19:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('food', '0003_auto_20220401_2256'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='ingredients',
            field=models.ManyToManyField(related_name='recipes', to='food.AmountIngredient', verbose_name='Ингредиенты рецепта'),
        ),
    ]