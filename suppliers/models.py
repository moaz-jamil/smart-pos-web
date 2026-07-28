from django.db import models

class Supplier(models.Model):
    business = models.ForeignKey('authentication.Business', on_delete=models.CASCADE, related_name='suppliers')
    company_name = models.CharField(max_length=200)
    contact_name = models.CharField(max_length=150, blank=True, null=True)
    phone = models.CharField(max_length=50)
    email = models.EmailField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    outstanding_balance = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.company_name} ({self.contact_name or 'N/A'})"
