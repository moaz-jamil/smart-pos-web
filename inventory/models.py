from django.db import models
from django.conf import settings

class Warehouse(models.Model):
    business = models.ForeignKey('authentication.Business', on_delete=models.CASCADE, related_name='warehouses')
    branch = models.ForeignKey('branches.Branch', on_delete=models.SET_NULL, null=True, blank=True, related_name='warehouses')
    name = models.CharField(max_length=150)
    location = models.TextField(blank=True, null=True)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class StockMovement(models.Model):
    TYPE_IN = 'IN'
    TYPE_OUT = 'OUT'
    TYPE_ADJUSTMENT = 'ADJUSTMENT'
    TYPE_TRANSFER = 'TRANSFER'

    MOVEMENT_TYPES = [
        (TYPE_IN, 'Stock In'),
        (TYPE_OUT, 'Stock Out'),
        (TYPE_ADJUSTMENT, 'Stock Adjustment'),
        (TYPE_TRANSFER, 'Stock Transfer'),
    ]

    business = models.ForeignKey('authentication.Business', on_delete=models.CASCADE, related_name='stock_movements')
    branch = models.ForeignKey('branches.Branch', on_delete=models.SET_NULL, null=True, blank=True, related_name='stock_movements')
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE, related_name='stock_movements')
    movement_type = models.CharField(max_length=20, choices=MOVEMENT_TYPES)
    quantity = models.IntegerField()
    reference_number = models.CharField(max_length=100, blank=True, null=True)
    batch_number = models.CharField(max_length=100, blank=True, null=True)
    expiry_date = models.DateField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.get_movement_type_display()} - {self.product.name} ({self.quantity})"
