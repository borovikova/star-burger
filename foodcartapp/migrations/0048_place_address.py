# Generated by Django 3.0.7 on 2021-03-28 07:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0047_auto_20210328_0757'),
    ]

    operations = [
        migrations.AddField(
            model_name='place',
            name='address',
            field=models.CharField(default='', max_length=150, verbose_name='адрес'),
            preserve_default=False,
        ),
    ]
