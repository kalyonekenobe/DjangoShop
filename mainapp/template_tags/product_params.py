from django import template
from mainapp.models import Cart, Customer, ContentType, CartProduct

register = template.Library()


@register.filter
def check_product_in_cart(product, user):
    if user.is_authenticated:
        owner = Customer.objects.get(user=user)
        cart = Cart.objects.get(owner=owner, in_order=False)
        content_type = ContentType.objects.get(model=product.__class__._meta.model_name)
        try:
            cart_product = True if cart.products.get(content_type=content_type, object_id=product.id) else False
        except CartProduct.DoesNotExist:
            cart_product = False
        return cart_product
    else:
        return True
