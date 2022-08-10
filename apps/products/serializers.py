from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from apps.products.models import Product, ProductCategory

User = get_user_model()


class ProductSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = (
            'id', 'title', 'category', 'image',
            'price', 'quantity', 'created_at', 'description',
            'gender', 'sizes', 'sale', 'new'
            )

    def get_image(self, obj):
        try:
            image = obj.image.url
        except:
            image = None
        return image

    def to_representation(self, instance):
        repres = super(ProductSerializer, self).to_representation(instance)
        repres['category'] = instance.category.title
        return repres


class ProductCategoriesSerializer(serializers.ModelSerializer):
    products = serializers.SerializerMethodField()

    class Meta:
        model = ProductCategory
        fields = ('id', 'title', 'products')

    def get_products(self, instance: ProductCategory):
        if self.context['order_value']:
            product_qs = instance.products.order_by(self.context['order_value'])
            return ProductSerializer(instance=product_qs, many=True).data
        else:
            product_qs = instance.products.all()
            return ProductSerializer(instance=product_qs, many=True).data


class RegistrationSerializer(serializers.ModelSerializer):
    """ Сериализация регистрации пользователя и создания нового. """
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )

    token = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'token']

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
