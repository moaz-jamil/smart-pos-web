from django.db import models
from django.conf import settings

class Customer(models.Model):
    business = models.ForeignKey('authentication.Business', on_delete=models.CASCADE, related_name='customers')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='customer_profile')
    name = models.CharField(max_length=150)
    phone = models.CharField(max_length=50)
    email = models.EmailField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    reward_points = models.IntegerField(default=0)
    wallet_balance = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    outstanding_balance = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.phone})"
