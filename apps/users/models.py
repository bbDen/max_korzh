from django.conf import settings
from django.contrib.auth.models import (
    AbstractBaseUser, PermissionsMixin
)

from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from phonenumber_field.validators import validate_international_phonenumber


from apps.users.managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=255, null=True)
    last_name = models.CharField(max_length=255, null=True)
    username = models.CharField(db_index=True, max_length=255, unique=True)
    email = models.EmailField(db_index=True, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_of_birth = models.DateField(verbose_name='Дата рождения', null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    phone_number = models.CharField(max_length=15, validators=[validate_international_phonenumber], unique=True,
                                    null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    def __str__(self):
        return self.email


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class Order(models.Model):
    """модель для заказов"""
    address = models.TextField(verbose_name='Адрес доставки')
    city = models.TextField(verbose_name='Город доставки')
    country = models.TextField(verbose_name='Страна доставки')
    customer = models.ForeignKey(to=User, on_delete=models.CASCADE, verbose_name='Заказчик')
    postcode = models.CharField(max_length=10, null=True)

    class Meta:
        verbose_name_plural = 'Заказы'
        verbose_name = 'Заказ'

    def __str__(self):
        return self.address


class OrderItem(models.Model):
    from apps.products.models import Product
    order = models.ForeignKey(to=Order, on_delete=models.CASCADE, related_name='order_items')
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE, related_name='order_items')
    product_price = models.IntegerField()


# request_body = [{'product': 12, 'size': 'XL'}, {'product': 435, 'size': 'XXl'}]
#
# p1=Product.objects.get(id=12)
# p2=Product.objects.get(id=435)
#
# order = Order.objects.create(country='aklsdjf', address='akljsdf;lja')
# item = OrderItem.objects.create(order=order, product=p1, )
# item = OrderItem.objects.create(order=order, product=p2)
