# Generated by Django 3.2.6 on 2021-08-14 17:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0004_auto_20210814_2012'),
    ]

    operations = [
        migrations.AlterField(
            model_name='smartphone',
            name='sd_card_volume',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name="Об'єм SD-картки"),
        ),
    ]