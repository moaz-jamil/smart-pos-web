from django.db import models
from django.conf import settings

class Branch(models.Model):
    business = models.ForeignKey('authentication.Business', on_delete=models.CASCADE, related_name='branches')
    name = models.CharField(max_length=150)
    code = models.CharField(max_length=50, blank=True, null=True)
    phone = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    manager = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='managed_branches')
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.business.name})"

    class Meta:
        verbose_name_plural = "Branches"
