from django.db import models

class ExpenseCategory(models.Model):
    business = models.ForeignKey('authentication.Business', on_delete=models.CASCADE, related_name='expense_categories')
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True, null=True)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Expense Categories"


class Expense(models.Model):
    business = models.ForeignKey('authentication.Business', on_delete=models.CASCADE, related_name='expenses')
    branch = models.ForeignKey('branches.Branch', on_delete=models.SET_NULL, null=True, blank=True, related_name='expenses')
    category = models.ForeignKey(ExpenseCategory, on_delete=models.CASCADE, related_name='expenses')
    title = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    expense_date = models.DateField()
    payment_method = models.CharField(max_length=50, default='Cash')
    receipt_image = models.ImageField(upload_to='expenses/', null=True, blank=True)
    notes = models.TextField(blank=True, null=True)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} - ${self.amount}"
