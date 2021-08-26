import json
from django.db import transaction
from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from .forms import *
from .mixins import *
from .utils import *


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
            'user': request.user,
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
        context['user'] = self.request.user
        return context
    

class CategoryDetailView(CategoryDetailMixin, DetailView):
    
    model = Category
    queryset = Category.objects.all()
    context_object_name = 'category'
    template_name = 'category_detail.html'
    slug_url_kwarg = 'slug'
    
    
class AddToCartView(CartMixin, View):

    def post(self, request, *args, **kwargs):
        ct_model, product_slug, data = kwargs.get('ct_model'), kwargs.get('slug'), True
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
            recalculate_cart(self.cart)
        else:
            data = False
        return HttpResponse(data)


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
        recalculate_cart(self.cart)
        return HttpResponseRedirect('/cart/')
    

class ClearCart(CartMixin, View):
    
    def get(self, request, *args, **kwargs):
        self.cart.products.clear()
        CartProduct.objects.filter(cart=self.cart).delete()
        self.cart.products_quantity = 0
        recalculate_cart(self.cart)
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
        recalculate_cart(self.cart)
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


class OrderView(CartMixin, View):
    
    def get(self, request, *args, **kwargs):
        context = {
            'cart': self.cart,
            'form': OrderForm(None),
        }
        return render(request, 'order.html', context)
    

class CreateOrderView(CartMixin, View):
    
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        form = OrderForm(request.POST or None)
        customer = Customer.objects.get(user=request.user)
        if form.is_valid():
            new_order = form.save(commit=False)
            new_order.customer = customer
            new_order.first_name = form.cleaned_data['first_name']
            new_order.last_name = form.cleaned_data['last_name']
            new_order.middle_name = form.cleaned_data['middle_name']
            new_order.phone = form.cleaned_data['phone']
            new_order.address = form.cleaned_data['address']
            new_order.email = form.cleaned_data['email']
            new_order.order_type = form.cleaned_data['order_type']
            new_order.comment = form.cleaned_data['comment']
            new_order.order_date = form.cleaned_data['order_date']
            self.cart.in_order = True
            recalculate_cart(self.cart)
            new_order.cart = self.cart
            new_order.save()
            customer.orders.add(new_order)
            customer.save()
            messages.add_message(request, messages.INFO, 'Дякуємо за замовлення!')
        context = {
            'order_id': new_order.id,
            'cart': new_order.cart,
        }
        return redirect('order_detail', order_id=new_order.id)
    

class OrderDetailView(CartMixin, DetailView):
    
    model = Order
    context_object_name = 'order'
    template_name = 'order_detail.html'
    queryset = Order.objects.all()
    pk_url_kwarg = 'order_id'
    
    