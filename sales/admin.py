from django.contrib import admin
from sales.models import Sale, SaleItem, Coupon

class SaleItemInline(admin.TabularInline):
    model = SaleItem
    extra = 0

@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ('invoice_number', 'customer', 'cashier', 'total_amount', 'payment_method', 'payment_status', 'created_at')
    search_fields = ('invoice_number', 'customer__name')
    list_filter = ('payment_method', 'payment_status', 'created_at')
    inlines = [SaleItemInline]

@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ('code', 'discount_percentage', 'min_purchase', 'valid_until', 'status')
    search_fields = ('code',)
