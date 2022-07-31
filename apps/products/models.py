from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class ProductCategory(models.Model):
    """Модель для категорий продуктов"""
    title = models.CharField(max_length=50, unique=True, verbose_name='Заголовок')

    class Meta:
        verbose_name_plural = 'Категории товаров'
        verbose_name = 'Категория товра'

    def __str__(self):
        return self.title


class Product(models.Model):
    """Модель для продуктов"""
    title = models.CharField(max_length=100, unique=True, verbose_name='Заголовок')
    category = models.ForeignKey(to=ProductCategory, on_delete=models.CASCADE, related_name='products')
    image = models.TextField(verbose_name='Изображение')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата размещения')
    quantity = models.IntegerField(verbose_name='Количество')
    price = models.IntegerField(verbose_name='Цена')
    description = models.TextField(max_length=500, verbose_name='Описание')
    gender = models.CharField(max_length=50, verbose_name='Пол', null=True)
    sale = models.IntegerField(null=True, verbose_name='Скидка')
    old_price = models.DecimalField(max_digits=5, decimal_places=2, null=True, verbose_name='Цена без скидки')

    class Meta:
        verbose_name_plural = 'Товары'
        verbose_name = 'Товар'

    def __str__(self):
        return self.title


class Comment(models.Model):
    """Модель для комментариев """
    post = models.ForeignKey(to=Product, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(to=User, on_delete=models.CASCADE, verbose_name='Автор комментария')
    content = models.TextField(max_length=255, verbose_name='Текст комментария')
    created_at = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey(to='self', null=True, blank=True, on_delete=models.CASCADE)

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return f'Comment by {self.author.email} on {self.post}'

    def children(self):
        return Comment.objects.filter(parent=self)

    @property
    def is_parent(self):
        if self.parent is not None:
            return False
        return True
