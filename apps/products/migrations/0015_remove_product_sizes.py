# Generated by Django 4.0.6 on 2022-08-04 13:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0014_alter_product_sizes'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='sizes',
        ),
    ]