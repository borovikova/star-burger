# Generated by Django 3.0.7 on 2021-02-24 20:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0052_auto_20210224_2052'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='called',
            field=models.DateTimeField(null=True, verbose_name='время звонка'),
        ),
        migrations.AlterField(
            model_name='order',
            name='delivered',
            field=models.DateTimeField(null=True, verbose_name='время доставки'),
        ),
    ]
