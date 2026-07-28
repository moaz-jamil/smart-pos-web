from django.contrib import admin
from products.models import Product, Category, Brand

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'business', 'status', 'created_at')
    search_fields = ('name',)

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('name', 'business', 'status', 'created_at')
    search_fields = ('name',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'barcode', 'sku', 'category', 'brand', 'purchase_price', 'selling_price', 'stock_quantity', 'status')
    search_fields = ('name', 'barcode', 'sku')
    list_filter = ('category', 'brand', 'status')
