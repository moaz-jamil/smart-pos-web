from django.db import models
from django.conf import settings

class Attendance(models.Model):
    business = models.ForeignKey('authentication.Business', on_delete=models.CASCADE, related_name='attendances')
    branch = models.ForeignKey('branches.Branch', on_delete=models.SET_NULL, null=True, blank=True, related_name='attendances')
    employee = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='attendances')
    date = models.DateField()
    clock_in = models.TimeField(null=True, blank=True)
    clock_out = models.TimeField(null=True, blank=True)
    working_hours = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.employee.username} - {self.date}"
