# Generated by Django 3.0.7 on 2021-07-19 15:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0048_place_address'),
    ]

    operations = [
        migrations.AlterField(
            model_name='place',
            name='address',
            field=models.CharField(max_length=150, unique=True, verbose_name='адрес'),
        ),
    ]
