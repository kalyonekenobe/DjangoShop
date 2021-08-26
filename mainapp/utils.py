from .models import *


def recalculate_cart(cart):
    cart_data = cart.products.aggregate(models.Sum('total_price'), models.Sum('quantity'))
    cart.total_price = cart_data['total_price__sum'] if cart_data['total_price__sum'] else Decimal.from_float(0.00)
    cart.products_quantity = cart_data['quantity__sum'] if cart_data['quantity__sum'] else 0
    cart.total_price = format(cart.total_price, '.2f')
    cart.save()