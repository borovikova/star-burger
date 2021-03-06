import itertools

from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import Prefetch, Sum
from django.utils import timezone
from geopy import distance
from phonenumber_field.modelfields import PhoneNumberField

from foodcartapp import geodata_functions


class Restaurant(models.Model):
    name = models.CharField('название', max_length=50, db_index=True)
    address = models.CharField('адрес', max_length=100, blank=True)
    contact_phone = models.CharField(
        'контактный телефон', max_length=50, blank=True)

    class Meta:
        verbose_name = 'ресторан'
        verbose_name_plural = 'рестораны'

    def __str__(self):
        return self.name


class ProductQuerySet(models.QuerySet):
    def available(self):
        return self.distinct().filter(menu_items__availability=True)


class ProductCategory(models.Model):
    name = models.CharField('название', max_length=50)

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField('название', max_length=50)
    category = models.ForeignKey(ProductCategory, null=True, blank=True, on_delete=models.SET_NULL,
                                 verbose_name='категория', related_name='products')
    price = models.DecimalField('цена', max_digits=8, decimal_places=2,
                                validators=[MinValueValidator(0)])
    image = models.ImageField('картинка')
    special_status = models.BooleanField(
        'спец.предложение', default=False, db_index=True)
    description = models.TextField('описание', max_length=200, blank=True)

    objects = ProductQuerySet.as_manager()

    class Meta:
        verbose_name = 'товар'
        verbose_name_plural = 'товары'

    def __str__(self):
        return self.name


class RestaurantMenuItem(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='menu_items',
                                   verbose_name="ресторан")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='menu_items',
                                verbose_name='продукт')
    availability = models.BooleanField(
        'в продаже', default=True, db_index=True)

    class Meta:
        verbose_name = 'пункт меню ресторана'
        verbose_name_plural = 'пункты меню ресторана'
        unique_together = [
            ['restaurant', 'product']
        ]

    def __str__(self):
        return f"{self.restaurant.name} - {self.product.name}"


class Place(models.Model):
    address = models.CharField('адрес', max_length=150, unique=True)
    latitude = models.FloatField('широта')
    longitude = models.FloatField('долгота')
    updated = models.DateTimeField('дата обновления', auto_now=True)


class OrderQuerySet(models.QuerySet):
    def fetch_restaurants(self):
        self = self.prefetch_related(
            Prefetch('order_items', queryset=OrderItem.objects.select_related('product')))
        menu_items = RestaurantMenuItem.objects.exclude(availability=False).select_related(
            'restaurant', 'product').order_by('restaurant_id')

        for order in self:
            order_coords = geodata_functions.get_coordinates_from_db_or_api(settings.YANDEX_API_KEY, order.address)
            order.products = [
                item.product.id for item in order.order_items.all()]
            order.restaurants = {}

            for restaurant, group in itertools.groupby(menu_items, lambda menu_item: menu_item.restaurant):
                products_in_restaurant = [menu_item.product.id for menu_item in group]

                if all(product in products_in_restaurant for product in order.products):
                    restaurant_coords = geodata_functions.get_coordinates_from_db_or_api(
                        settings.YANDEX_API_KEY, restaurant.address)
                    dist = None
                    if order_coords and restaurant_coords:
                        dist = round(
                            distance.distance(order_coords, restaurant_coords).km, 2)
                    order.restaurants[restaurant.address] = dist

            order.restaurants = {k: v for k, v in sorted(order.restaurants.items(), key=lambda item: item[1])}

        return self

    def total_price(self):
        return self.annotate(total_price=Sum('order_items__price'))


class Order(models.Model):
    ORDER_STATUS = (
        ('new', 'Новый'),
        ('preparation', 'Готовится'),
        ('in_delivery', 'У курьера'),
        ('finished', 'Доставлен'),
    )
    PAYMENT_METHOD = (
        ('cash', 'Наличные'),
        ('card', 'Картой на сайте'),
    )
    firstname = models.CharField('имя', max_length=50)
    lastname = models.CharField('фамилия', max_length=50)
    address = models.CharField('адрес', max_length=250)
    phonenumber = PhoneNumberField(db_index=True)
    order_status = models.CharField('статус заказа',
                                    max_length=15, choices=ORDER_STATUS, default='new', db_index=True)
    comment = models.TextField('комментарий', max_length=500, blank=True)
    created = models.DateTimeField('время создания', default=timezone.now, db_index=True)
    called = models.DateTimeField('время звонка', null=True, blank=True, db_index=True)
    delivered = models.DateTimeField('время доставки', null=True, blank=True, db_index=True)
    payment = models.CharField(
        'способ оплаты', max_length=15, choices=PAYMENT_METHOD, db_index=True)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.SET_NULL, null=True, blank=True, related_name='orders',
                                   verbose_name="ресторан")

    objects = OrderQuerySet.as_manager()

    class Meta:
        verbose_name = 'заказ'
        verbose_name_plural = 'заказы'

    def __str__(self):
        return f'{self.firstname} {self.lastname}, {self.address}'


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items',
                              verbose_name='заказ')
    product = models.ForeignKey(Product, on_delete=models.CASCADE,
                                related_name='order_items', verbose_name='продукт')
    quantity = models.PositiveSmallIntegerField()
    price = models.DecimalField('стоимость позиции', null=True, max_digits=8, decimal_places=2,
                                validators=[MinValueValidator(0)])

    class Meta:
        verbose_name = 'элемент заказа'
        verbose_name_plural = 'элементы заказа'
        unique_together = [
            ['order', 'product']
        ]

    def __str__(self):
        return f"{self.product.name}, {self.order}"
