# Generated by Django 3.2.6 on 2021-08-14 08:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0002_notebook_smartphone'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='for_unregistered_user',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='cart',
            name='in_order',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='smartphone',
            name='accumulator_volume',
            field=models.CharField(max_length=255, verbose_name="Об'єм батареї"),
        ),
    ]
