# Generated by Django 3.0.7 on 2021-02-18 20:57

from django.db import migrations


def calc_order_items_price(apps, schema_editor):
    OrderItem = apps.get_model('foodcartapp', 'OrderItem')
    OrderItem.objects.select_related('product').update(price=F('quantity') * F('product__price'))


class Migration(migrations.Migration):
    dependencies = [
        ('foodcartapp', '0044_auto_20210218_1936'),
    ]

    operations = [
        migrations.RunPython(calc_order_items_price),
    ]
