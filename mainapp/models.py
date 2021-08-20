from decimal import Decimal
from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.urls import reverse


def get_product_url(obj, view_name):
    ct_model = obj.__class__._meta.model_name
    ct_model = ct_model[:-1] + 'ies' if ct_model[-1] == 'y' else ct_model + 's'
    return reverse(view_name, kwargs={'ct_model': ct_model, 'slug': obj.slug})

# Makes whitespaces after every 3 characters
def modify_product_price_output(price):
    price = str(price)[::-1]
    price = [price[i:i + 3] for i in range(0, len(price), 3)]
    price = ' '.join(price)
    if price[3] == ' ':
        price = price[0:3] + price[4:len(price)]
    return price[::-1]


def count_models(*model_names):
    return [models.Count(model_name) for model_name in model_names]


class LatestProductsManager:

    @staticmethod
    def get_latest_products(*args, **kwargs):
        priority = kwargs.get('priority')
        products = []
        content_type_models = ContentType.objects.filter(model__in=args)

        for content_type_model in content_type_models:
            model_products = content_type_model.model_class()._base_manager.all().order_by('-id')[:5]
            products.extend(model_products)

        if priority:
            content_type_model = ContentType.objects.filter(model=priority)
            if content_type_model.exists() and (priority in args):
                return sorted(products, key=lambda x: x.__class__._meta.model_name.startswith(priority), reverse=True)

        return products


class LatestProducts:

    objects = LatestProductsManager()


class CategoryManager(models.Manager):
    
    CATEGORY_NAME_COUNT_NAME = {
        'Ноутбуки': 'notebook__count',
        'Смартфони': 'smartphone__count',
    }
    
    def get_queryset(self):
        return super().get_queryset()
    
    def get_categories(self):
        counted_models = count_models('notebook', 'smartphone')
        queryset = self.get_queryset().annotate(*counted_models)
        data = [
            dict(name=category.name, url=category.get_absolute_url(), count=getattr(category, self.CATEGORY_NAME_COUNT_NAME[category.name]))
            for category in queryset
        ]
        return data


class Category(models.Model):

    name = models.CharField(max_length=255, verbose_name="Назва категорії")
    slug = models.SlugField(unique=True)
    objects = CategoryManager()
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('category_detail', kwargs={'slug': self.slug})


class Product(models.Model):
    
    class Meta:
        abstract = True

    title = models.CharField(max_length=255, verbose_name="Назва")
    slug = models.SlugField(unique=True)
    category = models.ForeignKey(Category, verbose_name="Категорія", on_delete=models.CASCADE)
    image = models.ImageField(verbose_name="Зображення")
    description = models.TextField(null=True, verbose_name="Опис")
    price = models.DecimalField(max_digits=18, decimal_places=2, verbose_name="Ціна")

    def __str__(self):
        return self.title
    
    def modify_price(self):
        return modify_product_price_output(self.price)


class CartProduct(models.Model):

    user = models.ForeignKey('Customer', verbose_name="Покупець", on_delete=models.CASCADE)
    cart = models.ForeignKey('Cart', verbose_name="Кошик", on_delete=models.CASCADE, related_name="related_cart")
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    quantity = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(max_digits=18, decimal_places=2, verbose_name="Загальна ціна", default=0)

    def __str__(self):
        return "Товар: {}".format(self.content_object.title)
    
    def modify_price(self):
        return modify_product_price_output(self.total_price)
    
    def save(self, *args, **kwargs):
        self.total_price = int(self.quantity) * self.content_object.price
        super().save(*args, **kwargs)
        
    def get_model_name(self):
        return self.content_object.__class__._meta.model_name
        

class Cart(models.Model):

    owner = models.ForeignKey('Customer', null=True, verbose_name="Власник", on_delete=models.CASCADE)
    products = models.ManyToManyField(CartProduct, blank=True, related_name="related_products")
    products_quantity = models.PositiveIntegerField(default=0, verbose_name="Кількість товарів")
    total_price = models.DecimalField(max_digits=18, decimal_places=2, default=0, verbose_name="Загальна ціна")
    in_order = models.BooleanField(default=False)
    for_unregistered_user = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)
    
    def save(self, *args, **kwargs):
        cart_data = self.products.aggregate(models.Sum('total_price'), models.Sum('quantity'))
        self.total_price = cart_data['total_price__sum'] if cart_data['total_price__sum'] else Decimal.from_float(0.00)
        self.products_quantity = cart_data['quantity__sum'] if cart_data['quantity__sum'] else 0
        self.total_price = format(self.total_price, '.2f')
        super().save(*args, **kwargs)
    
    def modify_price(self):
        return modify_product_price_output(self.total_price)
    
    def get_cart_message(self):
        if self.products_quantity % 10 in range(2, 5) and self.products_quantity not in range(11, 20):
            word = "товари"
        elif self.products_quantity % 10 in range(5, 10) or self.products_quantity in range(11, 20) or self.products_quantity % 10 == 0:
            word = "товарів"
        else:
            word = "товар"
        return "Ви обрали {} {} на суму".format(self.products_quantity, word)


class Customer(models.Model):

    user = models.ForeignKey(User, verbose_name="Користувач", on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, verbose_name="Телефон", null=True)
    address = models.CharField(max_length=255, verbose_name="Адреса", null=True)

    def __str__(self):
        return "Покупець: {} {}".format(self.user.first_name, self.user.last_name)


class Notebook(Product):

    diagonal = models.CharField(max_length=255, verbose_name="Діагональ")
    display = models.CharField(max_length=255, verbose_name="Тип дисплею")
    processor_frequency = models.CharField(max_length=255, verbose_name="Частота процесора")
    ram = models.CharField(max_length=255, verbose_name="Оперативна пам'ять")
    video_card = models.CharField(max_length=255, verbose_name="Відеокарта")
    accumulator_volume = models.CharField(max_length=255, verbose_name="Час роботи від акумулятора")

    def __str__(self):
        return "{} : {}".format(self.category.name, self.title)

    def get_absolute_url(self):
        return get_product_url(self, 'product_detail')


class Smartphone(Product):

    diagonal = models.CharField(max_length=255, verbose_name="Діагональ")
    display = models.CharField(max_length=255, verbose_name="Тип дисплею")
    resolution = models.CharField(max_length=255, verbose_name="Роздільна якість")
    accumulator_volume = models.CharField(max_length=255, verbose_name="Об'єм батареї")
    ram = models.CharField(max_length=255, verbose_name="Оперативна пам'ять")
    sd_card = models.BooleanField(default=True)
    sd_card_volume = models.CharField(max_length=255, null=True, blank=True, verbose_name="Об'єм SD-картки")
    main_camera_size = models.CharField(max_length=255, verbose_name="Розмір головної камери")
    frontal_camera_size = models.CharField(max_length=255, verbose_name="Розмір фронтальної камери")

    def __str__(self):
        return "{} : {}".format(self.category.name, self.title)

    def get_absolute_url(self):
        return get_product_url(self, 'product_detail')
    
    