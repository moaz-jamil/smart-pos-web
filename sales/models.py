from django.db import models
from django.conf import settings

class Coupon(models.Model):
    business = models.ForeignKey('authentication.Business', on_delete=models.CASCADE, related_name='coupons')
    code = models.CharField(max_length=50, unique=True)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    min_purchase = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    valid_until = models.DateField()
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.code} ({self.discount_percentage}%)"


class Sale(models.Model):
    METHOD_CASH = 'CASH'
    METHOD_CARD = 'CARD'
    METHOD_SPLIT = 'SPLIT'

    PAYMENT_METHOD_CHOICES = [
        (METHOD_CASH, 'Cash'),
        (METHOD_CARD, 'Card'),
        (METHOD_SPLIT, 'Split Payment'),
    ]

    STATUS_PAID = 'PAID'
    STATUS_PARTIAL = 'PARTIAL'
    STATUS_UNPAID = 'UNPAID'
    STATUS_REFUNDED = 'REFUNDED'

    PAYMENT_STATUS_CHOICES = [
        (STATUS_PAID, 'Paid'),
        (STATUS_PARTIAL, 'Partial'),
        (STATUS_UNPAID, 'Unpaid'),
        (STATUS_REFUNDED, 'Refunded'),
    ]

    business = models.ForeignKey('authentication.Business', on_delete=models.CASCADE, related_name='sales')
    branch = models.ForeignKey('branches.Branch', on_delete=models.SET_NULL, null=True, blank=True, related_name='sales')
    customer = models.ForeignKey('customers.Customer', on_delete=models.SET_NULL, null=True, blank=True, related_name='sales')
    cashier = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='processed_sales')
    coupon = models.ForeignKey(Coupon, on_delete=models.SET_NULL, null=True, blank=True, related_name='sales')
    invoice_number = models.CharField(max_length=100, unique=True)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    tax_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    discount_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    paid_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    change_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, default=METHOD_CASH)
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default=STATUS_PAID)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Invoice #{self.invoice_number} - ${self.total_amount}"


class SaleItem(models.Model):
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    unit_price = models.DecimalField(max_digits=12, decimal_places=2)
    tax_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    discount_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    subtotal = models.DecimalField(max_digits=12, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"
