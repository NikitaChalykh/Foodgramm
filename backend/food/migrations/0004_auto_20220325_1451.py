# Generated by Django 2.2.16 on 2022-03-25 11:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('food', '0003_shoppinglist'),
    ]

    operations = [
        migrations.RenameField(
            model_name='amountingredient',
            old_name='number',
            new_name='amount',
        ),
    ]