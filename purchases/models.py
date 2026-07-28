from django.db import models
from django.conf import settings

class Purchase(models.Model):
    PAYMENT_PAID = 'PAID'
    PAYMENT_PARTIAL = 'PARTIAL'
    PAYMENT_UNPAID = 'UNPAID'

    PAYMENT_STATUS_CHOICES = [
        (PAYMENT_PAID, 'Paid'),
        (PAYMENT_PARTIAL, 'Partial'),
        (PAYMENT_UNPAID, 'Unpaid'),
    ]

    RECEIVED_STATUS_RECEIVED = 'RECEIVED'
    RECEIVED_STATUS_PENDING = 'PENDING'

    RECEIVED_STATUS_CHOICES = [
        (RECEIVED_STATUS_RECEIVED, 'Received'),
        (RECEIVED_STATUS_PENDING, 'Pending'),
    ]

    business = models.ForeignKey('authentication.Business', on_delete=models.CASCADE, related_name='purchases')
    branch = models.ForeignKey('branches.Branch', on_delete=models.SET_NULL, null=True, blank=True, related_name='purchases')
    supplier = models.ForeignKey('suppliers.Supplier', on_delete=models.CASCADE, related_name='purchases')
    invoice_number = models.CharField(max_length=100, unique=True)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    discount_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    tax_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    paid_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default=PAYMENT_UNPAID)
    received_status = models.CharField(max_length=20, choices=RECEIVED_STATUS_CHOICES, default=RECEIVED_STATUS_PENDING)
    notes = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"PO #{self.invoice_number} - {self.supplier.company_name}"


class PurchaseItem(models.Model):
    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    unit_cost = models.DecimalField(max_digits=12, decimal_places=2)
    total_cost = models.DecimalField(max_digits=12, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"
