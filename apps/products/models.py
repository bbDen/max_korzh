from django.contrib.auth import get_user_model
from django.db import models


class ProductCategory(models.Model):
    """Модель для категорий продуктов"""
    title = models.CharField(max_length=50, unique=True, verbose_name='Заголовок')

    class Meta:
        verbose_name_plural = 'Категории товаров'
        verbose_name = 'Категория товара'

    def __str__(self):
        return self.title


class Product(models.Model):
    """Модель для продуктов"""
    title = models.CharField(max_length=100, unique=True, verbose_name='Заголовок')
    category = models.ForeignKey(to=ProductCategory, on_delete=models.CASCADE, related_name='products')
    image = models.ImageField(verbose_name='Изображение')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата размещения')
    quantity = models.IntegerField(verbose_name='Количество')
    price = models.IntegerField(verbose_name='Цена')
    description = models.TextField(max_length=500, verbose_name='Описание')
    gender = models.CharField(max_length=50, verbose_name='Пол', null=True)
    sale = models.IntegerField(null=True, verbose_name='Скидка', blank=True)
    new = models.BooleanField(default=True)
    sizes = ['XXS', 'XS', 'S', 'M', 'L', 'XL']

    class Meta:
        verbose_name_plural = 'Товары'
        verbose_name = 'Товар'

    def __str__(self):
        return self.title
