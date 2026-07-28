from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from authentication.models import User, Business

@admin.register(Business)
class BusinessAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'tax_number', 'status', 'created_at')
    search_fields = ('name', 'email', 'phone', 'tax_number')
    list_filter = ('status', 'created_at')


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'business', 'branch', 'is_staff')
    list_filter = ('role', 'is_staff', 'is_superuser', 'status')
    fieldsets = BaseUserAdmin.fieldsets + (
        ('SmartPOS Extra Info', {'fields': ('role', 'business', 'branch', 'phone', 'profile_picture', 'status')}),
    )
