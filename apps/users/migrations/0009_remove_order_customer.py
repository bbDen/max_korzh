# Generated by Django 4.0.6 on 2022-08-04 13:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_alter_order_customer'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='customer',
        ),
    ]
