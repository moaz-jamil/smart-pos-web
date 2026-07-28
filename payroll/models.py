from django.db import models
from django.conf import settings

class Payroll(models.Model):
    STATUS_PAID = 'PAID'
    STATUS_PENDING = 'PENDING'

    PAYMENT_STATUS_CHOICES = [
        (STATUS_PAID, 'Paid'),
        (STATUS_PENDING, 'Pending'),
    ]

    business = models.ForeignKey('authentication.Business', on_delete=models.CASCADE, related_name='payrolls')
    employee = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='payrolls')
    month = models.IntegerField()
    year = models.IntegerField()
    base_salary = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    bonus = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    deductions = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    net_salary = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default=STATUS_PENDING)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.employee.username} - {self.month}/{self.year} - ${self.net_salary}"
