from django.contrib import admin
from . models import Product, Cart

# Register your models here.


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'price']
    ordering = ['price',]
    search_fields = ['name',]


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['id', 'user',]
    list_filter = ['user',]
    search_fields = ['user',]


admin.site.site_header = "Product Review Admin"
