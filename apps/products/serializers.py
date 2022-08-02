from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from apps.products.models import Comment, Product, ProductCategory, TestModel

User = get_user_model()


class TestModelSerializer(serializers.ModelSerializer):
    image = SerializerMethodField()
    music = SerializerMethodField()
    class Meta:
        model = TestModel
        fields = '__all__'

    def get_image(self, obj):
        try:
            image = obj.image.url
        except:
            image = None
        return image

    def get_music(self, obj):
        try:
            music = obj.music.url
        except:
            music = None
        return music


class ProductSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField()

    class Meta:
        model = Product
        fields = ('id', 'title', 'category', 'image', 'price', 'quantity', 'created_at', 'description', 'gender',
                  'old_price', 'sale'
                  )


class CommentSerializer(serializers.ModelSerializer):
    reply_count = SerializerMethodField()
    author = SerializerMethodField()

    class Meta:
        model = Comment
        fields = ('content', 'parent', 'author', 'reply_count', 'post')

    def get_reply_count(self, obj):
        if obj.is_parent:
            return obj.children().count()
        return 0

    def get_author(self, obj):
        return obj.author.username


class ProductCategoriesSerializer(serializers.ModelSerializer):
    products = ProductSerializer(read_only=True, many=True)

    class Meta:
        model = ProductCategory
        fields = ('id', 'title', 'products')


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
