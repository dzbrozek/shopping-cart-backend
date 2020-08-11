from django.contrib import admin
from products.models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'uuid', 'name', 'price')
    search_fields = ('id', 'uuid', 'name')
