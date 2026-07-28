from django.db import models

class Category(models.Model):
    business = models.ForeignKey('authentication.Business', on_delete=models.CASCADE, related_name='categories')
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='categories/', null=True, blank=True)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"


class Brand(models.Model):
    business = models.ForeignKey('authentication.Business', on_delete=models.CASCADE, related_name='brands')
    name = models.CharField(max_length=150)
    logo = models.ImageField(upload_to='brands/', null=True, blank=True)
    description = models.TextField(blank=True, null=True)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    business = models.ForeignKey('authentication.Business', on_delete=models.CASCADE, related_name='products')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True, blank=True, related_name='products')
    supplier = models.ForeignKey('suppliers.Supplier', on_delete=models.SET_NULL, null=True, blank=True, related_name='products')
    name = models.CharField(max_length=200)
    barcode = models.CharField(max_length=100, unique=True)
    sku = models.CharField(max_length=100, unique=True)
    purchase_price = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    selling_price = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    tax_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)  # percentage
    discount_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0.00) # percentage
    stock_quantity = models.IntegerField(default=0)
    min_stock_level = models.IntegerField(default=5)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='products/', null=True, blank=True)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def is_low_stock(self):
        return self.stock_quantity <= self.min_stock_level

    @property
    def final_price(self):
        discount_amount = (self.selling_price * self.discount_rate) / 100
        tax_amount = ((self.selling_price - discount_amount) * self.tax_rate) / 100
        return self.selling_price - discount_amount + tax_amount

    def __str__(self):
        return f"{self.name} ({self.sku})"
