# Generated by Django 3.2.6 on 2021-08-19 10:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0007_alter_cart_owner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='address',
            field=models.CharField(max_length=255, null=True, verbose_name='Адреса'),
        ),
        migrations.AlterField(
            model_name='customer',
            name='phone',
            field=models.CharField(max_length=20, null=True, verbose_name='Телефон'),
        ),
    ]
