from django.urls import path
from .views import *

urlpatterns = [
    path('', BaseView.as_view(), name='base'),
    path('products/<str:ct_model>/<str:slug>/', ProductDetailView.as_view(), name='product_detail'),
    path('products/<str:slug>/', CategoryDetailView.as_view(), name='category_detail'),
    path('cart/', CartView.as_view(), name='cart'),
    path('add-to-cart/<str:ct_model>/<str:slug>/', AddToCartView.as_view(), name='add_to_cart'),
    path('remove-from-cart/<str:ct_model>/<str:slug>/', DeleteFromCartView.as_view(), name='remove_from_cart'),
    path('clear-cart/', ClearCart.as_view(), name='clear_cart'),
    path('change-product-quantity/<str:ct_model>/<str:slug>/', ChangeProductQuantityView.as_view(), name='change_product_quantity'),
]