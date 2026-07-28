from django.db import models
from django.contrib.auth.models import AbstractUser

class Business(models.Model):
    name = models.CharField(max_length=255)
    logo = models.ImageField(upload_to='business_logos/', null=True, blank=True)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=50, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    tax_number = models.CharField(max_length=100, blank=True, null=True)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Businesses"


class User(AbstractUser):
    ROLE_SUPER_ADMIN = 'SUPER_ADMIN'
    ROLE_ADMIN = 'ADMIN'
    ROLE_EMPLOYEE = 'EMPLOYEE'
    ROLE_CUSTOMER = 'CUSTOMER'

    ROLE_CHOICES = [
        (ROLE_SUPER_ADMIN, 'Super Admin'),
        (ROLE_ADMIN, 'Admin (Business Owner)'),
        (ROLE_EMPLOYEE, 'Employee (Cashier)'),
        (ROLE_CUSTOMER, 'Customer'),
    ]

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=ROLE_EMPLOYEE)
    business = models.ForeignKey(Business, on_delete=models.CASCADE, null=True, blank=True, related_name='users')
    branch = models.ForeignKey('branches.Branch', on_delete=models.SET_NULL, null=True, blank=True, related_name='users')
    phone = models.CharField(max_length=30, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def is_super_admin(self):
        return self.role == self.ROLE_SUPER_ADMIN or self.is_superuser

    def is_admin(self):
        return self.role in [self.ROLE_ADMIN, self.ROLE_SUPER_ADMIN] or self.is_superuser

    def is_employee(self):
        return self.role == self.ROLE_EMPLOYEE

    def is_customer(self):
        return self.role == self.ROLE_CUSTOMER

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
