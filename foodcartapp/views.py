import json

from django.http import JsonResponse
from django.templatetags.static import static
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Order, OrderItem, Product


def banners_list_api(request):
    # FIXME move data to db?
    return JsonResponse([
        {
            'title': 'Burger',
            'src': static('burger.jpg'),
            'text': 'Tasty Burger at your door step',
        },
        {
            'title': 'Spices',
            'src': static('food.jpg'),
            'text': 'All Cuisines',
        },
        {
            'title': 'New York',
            'src': static('tasty.jpg'),
            'text': 'Food is incomplete without a tasty dessert',
        }
    ], safe=False, json_dumps_params={
        'ensure_ascii': False,
        'indent': 4,
    })


def product_list_api(request):
    products = Product.objects.select_related('category').available()

    dumped_products = []
    for product in products:
        dumped_product = {
            'id': product.id,
            'name': product.name,
            'price': product.price,
            'special_status': product.special_status,
            'description': product.description,
            'category': {
                'id': product.category.id,
                'name': product.category.name,
            },
            'image': product.image.url,
            'restaurant': {
                'id': product.id,
                'name': product.name,
            }
        }
        dumped_products.append(dumped_product)
    return JsonResponse(dumped_products, safe=False, json_dumps_params={
        'ensure_ascii': False,
        'indent': 4,
    })


@api_view(['POST'])
def register_order(request):
    raw_order = request.data
    if 'products' not in raw_order.keys() \
            or not isinstance(raw_order['products'], list) \
            or not raw_order['products']:
        return Response({'Error': 'Products keys not found in request or not list'},
                        status=status.HTTP_417_EXPECTATION_FAILED)

    order = Order.objects.create(
        first_name=raw_order['firstname'],
        last_name=raw_order['lastname'],
        phone=raw_order['phonenumber'],
        address=raw_order['address'],
    )
    items = OrderItem.objects.bulk_create(
        [OrderItem(
            product_id=product['product'],
            quantity=product['quantity'],
            order_id=order.id)
            for product in raw_order['products']]
    )
    return JsonResponse({})
