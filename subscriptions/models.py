from django.db import models

class SubscriptionPlan(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    max_branches = models.IntegerField(default=1)
    max_users = models.IntegerField(default=5)
    max_products = models.IntegerField(default=500)
    description = models.TextField(blank=True, null=True)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - ${self.price}"


class BusinessSubscription(models.Model):
    business = models.ForeignKey('authentication.Business', on_delete=models.CASCADE, related_name='subscriptions')
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.business.name} - {self.plan.name}"
