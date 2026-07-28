from django.db import models
from django.conf import settings

class EmployeeProfile(models.Model):
    business = models.ForeignKey('authentication.Business', on_delete=models.CASCADE, related_name='employee_profiles')
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='employee_profile')
    designation = models.CharField(max_length=100, default='Cashier')
    salary = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    join_date = models.DateField(auto_now_add=True)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username} - {self.designation}"
