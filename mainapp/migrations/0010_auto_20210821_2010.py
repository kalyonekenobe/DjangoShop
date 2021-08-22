# Generated by Django 3.2.6 on 2021-08-21 17:10

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0009_auto_20210820_1713'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=255, verbose_name="Ім'я")),
                ('last_name', models.CharField(max_length=255, verbose_name='Прізвище')),
                ('middle_name', models.CharField(blank=True, max_length=255, null=True, verbose_name='По-батькові')),
                ('phone', models.CharField(max_length=20, verbose_name='Телефон')),
                ('address', models.CharField(blank=True, max_length=1024, null=True, verbose_name='Адреса')),
                ('email', models.CharField(blank=True, max_length=255, null=True, verbose_name='E-mail')),
                ('status', models.CharField(choices=[('new', 'Нове замовлення'), ('in_progress', 'В процесі обробки'), ('is_ready', 'Готовий до відправлення'), ('completed', 'Замовлення виконане')], default='new', max_length=100, verbose_name='Стан замовлення')),
                ('order_type', models.CharField(choices=[('self-pickup', 'Самовивіз'), ('delivery', 'Доставка')], default='delivery', max_length=100, verbose_name='Тип замовлення')),
                ('comment', models.TextField(blank=True, null=True, verbose_name='Коментар до замовлення')),
                ('order_datetime', models.DateTimeField(auto_now=True, verbose_name='Дата створення')),
                ('order_date', models.DateField(default=django.utils.timezone.now, verbose_name='Дата отримання замовлення')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='related_customer', to='mainapp.customer', verbose_name='Замовник')),
            ],
        ),
        migrations.AddField(
            model_name='customer',
            name='orders',
            field=models.ManyToManyField(related_name='related_orders', to='mainapp.Order', verbose_name='Замовлення користувача'),
        ),
    ]
