# Generated by Django 4.0.6 on 2022-08-04 13:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0015_remove_product_sizes'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='sizes',
            field=models.CharField(choices=[('XXS', 'XXS'), ('XS', 'XS'), ('S', 'S'), ('M', 'M'), ('L', 'L'), ('XL', 'XL')], default='XS', max_length=5),
        ),
    ]
