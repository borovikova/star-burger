# Generated by Django 3.0.7 on 2021-02-17 18:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0041_auto_20210211_1836'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='first_name',
            new_name='firstname',
        ),
        migrations.RenameField(
            model_name='order',
            old_name='last_name',
            new_name='lastname',
        ),
        migrations.RenameField(
            model_name='order',
            old_name='phone',
            new_name='phonenumber',
        ),
    ]
