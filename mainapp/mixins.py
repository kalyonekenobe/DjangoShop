from django.views.generic.detail import SingleObjectMixin

from .models import Category


class CategoryDetailMixin(SingleObjectMixin):

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories_list'] = Category.objects.get_categories()
        products_quantity = 0
        for category in context['categories_list']:
            products_quantity += category['count']
        context['products_quantity'] = products_quantity
        return context