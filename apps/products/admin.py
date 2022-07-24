from django.contrib import admin

# Register your models here.
from apps.products.models import Products, ProductCategories


@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    pass

@admin.register(ProductCategories)
class ProductCategoriesAdmin(admin.ModelAdmin):
    pass