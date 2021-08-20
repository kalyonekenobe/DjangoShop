import json
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.views.generic import DetailView, ListView, View
from django.contrib.contenttypes.models import ContentType
from .models import Notebook, Smartphone, Category, LatestProducts, Customer, Cart, CartProduct
from .mixins import *


class BaseView(CartMixin, View):
    
    def get(self, request, *args, **kwargs):
        categories_list = Category.objects.get_categories()
        products_quantity = 0
        for category in categories_list:
            products_quantity += category['count']
        products = LatestProducts.objects.get_latest_products('notebook', 'smartphone', priority='notebook')
        context = {
            'categories_list': categories_list,
            'products_quantity': products_quantity,
            'products': products,
            'cart': self.cart,
        }
        return render(request, 'base.html', context)


class ProductDetailView(CartMixin, DetailView):

    context_object_name = 'product'
    template_name = 'product_detail.html'
    slug_url_kwarg = 'slug'

    CT_MODEL_CLASS = {
        'notebooks': Notebook,
        'smartphones': Smartphone
    }

    def dispatch(self, request, *args, **kwargs):
        self.model = self.CT_MODEL_CLASS[kwargs['ct_model']]
        self.queryset = self.model._base_manager.all()
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ct_model'] = self.model._meta.model_name
        context['cart'] = self.cart
        return context
    

class CategoryDetailView(CategoryDetailMixin, DetailView):
    
    model = Category
    queryset = Category.objects.all()
    context_object_name = 'category'
    template_name = 'category_detail.html'
    slug_url_kwarg = 'slug'
    
    
class AddToCartView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        ct_model, product_slug = kwargs.get('ct_model'), kwargs.get('slug')
        customer = Customer.objects.get(user=request.user)
        content_type = ContentType.objects.get(model=ct_model)
        product = content_type.model_class().objects.get(slug=product_slug)
        cart_product, created = CartProduct.objects.get_or_create(
            user=customer, cart=self.cart, content_type=content_type, object_id=product.id
        )
        if cart_product.quantity < 999:
            if created:
                self.cart.products.add(cart_product)
            else:
                cart_product.quantity += 1
                cart_product.save()
            self.cart.save()
        ct_model_path_name = ct_model[:-1] + 'ies' if ct_model[-1] == 'y' else ct_model + 's'
        redirect_path = f'/products/{ct_model_path_name}/{product_slug}'
        return HttpResponseRedirect(redirect_path)


class DeleteFromCartView(CartMixin, View):
    
    def get(self, request, *args, **kwargs):
        ct_model, product_slug = kwargs.get('ct_model'), kwargs.get('slug')
        content_type = ContentType.objects.get(model=ct_model)
        product = content_type.model_class().objects.get(slug=product_slug)
        cart_product = CartProduct.objects.get(
            user=self.cart.owner, cart=self.cart, content_type=content_type, object_id=product.id
        )
        if cart_product:
            self.cart.products.remove(cart_product)
            cart_product.delete()
        self.cart.save()
        return HttpResponseRedirect('/cart/')
    

class ClearCart(CartMixin, View):
    
    def get(self, request, *args, **kwargs):
        self.cart.products.clear()
        CartProduct.objects.filter(cart=self.cart).delete()
        self.cart.products_quantity = 0
        self.cart.save()
        return HttpResponseRedirect('/cart/')
    

class ChangeProductQuantityView(CartMixin, View):
    
    def post(self, request, *args, **kwargs):
        ct_model, product_slug = kwargs.get('ct_model'), kwargs.get('slug')
        content_type = ContentType.objects.get(model=ct_model)
        product = content_type.model_class().objects.get(slug=product_slug)
        cart_product = CartProduct.objects.get(
            user=self.cart.owner, cart=self.cart, content_type=content_type, object_id=product.id
        )
        cart_product.quantity = request.POST['quantity']
        cart_product.total_price = int(request.POST['quantity']) * product.price
        cart_product.save()
        self.cart.save()
        data = {
            'cart_total_price': str(self.cart.modify_price()),
            'product_total_price': str(cart_product.modify_price()),
            'cart_products_quantity': str(self.cart.products_quantity),
            'cart_message': str(self.cart.get_cart_message()),
        }
        return HttpResponse(json.dumps(data))


class CartView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        categories = Category.objects.get_categories()
        context = {
            'cart': self.cart,
            'categories_list': categories,
        }
        return render(request, 'cart.html', context)
    