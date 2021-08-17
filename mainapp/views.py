from django.shortcuts import render
from django.views.generic import DetailView, ListView, View
from .models import Notebook, Smartphone, Category, Product
from .mixins import CategoryDetailMixin


class BaseView(View):
    
    def get(self, request, *args, **kwargs):
        categories_list = Category.objects.get_categories()
        products_quantity = 0
        for category in categories_list:
            products_quantity += category['count']
        return render(request, 'base.html', {'categories_list': categories_list, 'products_quantity': products_quantity})


class ProductDetailView(DetailView):

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
    

class CategoryDetailView(CategoryDetailMixin, DetailView):
    
    model = Category
    queryset = Category.objects.all()
    context_object_name = 'category'
    template_name = 'category_detail.html'
    slug_url_kwarg = 'slug'
    