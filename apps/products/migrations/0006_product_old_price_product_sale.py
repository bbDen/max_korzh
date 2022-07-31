# Generated by Django 4.0.6 on 2022-07-31 08:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0005_alter_product_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='old_price',
            field=models.DecimalField(decimal_places=2, max_digits=5, null=True, verbose_name='Цена без скидки'),
        ),
        migrations.AddField(
            model_name='product',
            name='sale',
            field=models.IntegerField(null=True, verbose_name='Скидка'),
        ),
    ]