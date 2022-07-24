from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from apps.products.models import Comment, Products, ProductCategories


class ProductSerializer(serializers.ModelSerializer):
    image = SerializerMethodField()
    category = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Products
        fields = ('id', 'title', 'category', 'image', 'price', 'quantity', 'created_at', 'description')

    def get_image(self, obj):
        try:
            image = obj.image.url
        except:
            image = None
        return image

    #  qs = Products.objects.prefetch_related('products')


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
        model = ProductCategories
        fields = ('id', 'title', 'products')
