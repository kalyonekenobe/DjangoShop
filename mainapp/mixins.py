from django.views.generic.detail import SingleObjectMixin
from django.views.generic import View, DetailView, ListView
from .models import *


class CartMixin(View):
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            customer = Customer.objects.filter(user=request.user).first()
            if not customer:
                customer = Customer.objects.create(user=request.user)
            cart = Cart.objects.filter(owner=customer, in_order=False).first()
            if not cart:
                cart = Cart.objects.create(owner=customer)
        else:
            cart = Cart.objects.filter(for_unregistered_user=True).first()
            if not cart:
                cart = Cart.objects.create(for_unregistered_user=True)
        self.cart = cart
        return super().dispatch(request, *args, **kwargs)


class CategoryDetailMixin(SingleObjectMixin, CartMixin):
    
    PRODUCTS_CLASS_BY_CATEGORY_SLUG = {
        'notebooks': Notebook,
        'smartphones': Smartphone,
    }
    
    def get_products_by_category(self, context):
        category_slug = context['category'].slug
        products_class = self.PRODUCTS_CLASS_BY_CATEGORY_SLUG[category_slug]
        products = products_class.objects.all()
        return products

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories_list'] = Category.objects.get_categories()
        products_quantity = 0
        for category in context['categories_list']:
            products_quantity += category['count']
        context['products_quantity'] = products_quantity
        context['cart'] = self.cart
        context['products'] = self.get_products_by_category(context)
        context['user'] = self.request.user
        return context
        