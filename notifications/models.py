from django.db import models
from django.conf import settings

class Notification(models.Model):
    TYPE_LOW_STOCK = 'LOW_STOCK'
    TYPE_ORDER = 'ORDER'
    TYPE_PURCHASE = 'PURCHASE'
    TYPE_SYSTEM = 'SYSTEM'

    TYPE_CHOICES = [
        (TYPE_LOW_STOCK, 'Low Stock'),
        (TYPE_ORDER, 'New Order'),
        (TYPE_PURCHASE, 'Purchase Received'),
        (TYPE_SYSTEM, 'System Announcement'),
    ]

    business = models.ForeignKey('authentication.Business', on_delete=models.CASCADE, related_name='notifications', null=True, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications', null=True, blank=True)
    title = models.CharField(max_length=200)
    message = models.TextField()
    notification_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default=TYPE_SYSTEM)
    is_read = models.BooleanField(default=False)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"[{self.get_notification_type_display()}] {self.title}"
