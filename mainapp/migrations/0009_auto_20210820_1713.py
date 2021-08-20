# Generated by Django 3.2.6 on 2021-08-20 14:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0008_auto_20210819_1324'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='total_price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=18, verbose_name='Загальна ціна'),
        ),
        migrations.AlterField(
            model_name='cartproduct',
            name='total_price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=18, verbose_name='Загальна ціна'),
        ),
        migrations.AlterField(
            model_name='notebook',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=18, verbose_name='Ціна'),
        ),
        migrations.AlterField(
            model_name='smartphone',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=18, verbose_name='Ціна'),
        ),
    ]