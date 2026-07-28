from django.db import models

class BusinessSetting(models.Model):
    business = models.OneToOneField('authentication.Business', on_delete=models.CASCADE, related_name='settings')
    currency_symbol = models.CharField(max_length=10, default='$')
    tax_number = models.CharField(max_length=100, blank=True, null=True)
    tax_rate = models.DecimalField(max_digits=5, decimal_places=2, default=5.00)
    receipt_header = models.TextField(default='Thank you for shopping with SmartPOS!')
    receipt_footer = models.TextField(default='Please visit us again. Returns accepted within 7 days.')
    theme = models.CharField(max_length=20, default='dark')
    language = models.CharField(max_length=10, default='en')
    low_stock_threshold = models.IntegerField(default=5)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Settings for {self.business.name}"
