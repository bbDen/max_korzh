from django.contrib import admin

# Register your models here.
from apps.products.models import Product, ProductCategory


@admin.register(Product)
class ProductsAdmin(admin.ModelAdmin):
    pass


@admin.register(ProductCategory)
class ProductCategoriesAdmin(admin.ModelAdmin):
    pass
