# Generated by Django 4.0.6 on 2022-08-02 14:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0007_alter_product_old_price'),
    ]

    operations = [
        migrations.CreateModel(
            name='TestModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('test_image', models.ImageField(upload_to='')),
            ],
            options={
                'verbose_name': 'Тестовая модель',
                'verbose_name_plural': 'Тестовая модель',
            },
        ),
    ]
