from django.contrib import admin

from apps.products.models import Product, ProductCategory
#from apps.users.models import Order


@admin.register(Product)
class ProductsAdmin(admin.ModelAdmin):
    pass


@admin.register(ProductCategory)
class ProductCategoriesAdmin(admin.ModelAdmin):
    pass


# @admin.register(Order)
# class MusicAdmin(admin.ModelAdmin):
#     pass
