# Generated by Django 2.2.16 on 2022-03-30 10:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('food', '0006_auto_20220330_1258'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='image',
            field=models.ImageField(blank=True, help_text='Загрузите сюда картинку вашего рецепта', upload_to='recipes/', verbose_name='Картинка рецепта'),
        ),
    ]
