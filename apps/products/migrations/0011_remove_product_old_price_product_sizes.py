# Generated by Django 4.0.6 on 2022-08-04 12:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0010_product_new'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='old_price',
        ),
        migrations.AddField(
            model_name='product',
            name='sizes',
            field=models.IntegerField(choices=[(1, 'XS'), (2, 'S'), (3, 'M'), (4, 'L'), (5, 'XL'), (6, 'XXS')], default=3),
        ),
    ]
