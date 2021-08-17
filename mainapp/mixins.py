from django.views.generic.detail import SingleObjectMixin

from .models import Category


class CategoryDetailMixin(SingleObjectMixin):

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories_list'] = Category.objects.get_categories()
        return context