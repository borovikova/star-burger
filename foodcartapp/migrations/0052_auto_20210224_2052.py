# Generated by Django 3.0.7 on 2021-02-24 20:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0051_auto_20210224_2049'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='called',
            field=models.DateTimeField(blank=True, verbose_name='время звонка'),
        ),
        migrations.AlterField(
            model_name='order',
            name='delivered',
            field=models.DateTimeField(blank=True, verbose_name='время доставки'),
        ),
    ]
