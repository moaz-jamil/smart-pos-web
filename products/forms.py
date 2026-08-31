from django import forms
from products.models import Product, Category, Brand

class CategoryForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['status'].initial = True
        self.fields['description'].required = False
        self.fields['image'].required = False

    class Meta:
        model = Category
        fields = ['name', 'description', 'image', 'status']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'status': forms.CheckboxInput(attrs={'class': 'form-check-input', 'checked': True}),
        }


class BrandForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['status'].initial = True
        self.fields['description'].required = False
        self.fields['logo'].required = False

    class Meta:
        model = Brand
        fields = ['name', 'description', 'logo', 'status']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'logo': forms.FileInput(attrs={'class': 'form-control'}),
            'status': forms.CheckboxInput(attrs={'class': 'form-check-input', 'checked': True}),
        }


class ProductForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['status'].initial = True
        self.fields['barcode'].required = False
        self.fields['sku'].required = False
        self.fields['brand'].required = False
        self.fields['supplier'].required = False
        self.fields['category'].required = False
        self.fields['image'].required = False
        self.fields['description'].required = False
        self.fields['tax_rate'].required = False
        self.fields['tax_rate'].initial = 0.00
        self.fields['discount_rate'].required = False
        self.fields['discount_rate'].initial = 0.00
        self.fields['min_stock_level'].required = False
        self.fields['min_stock_level'].initial = 5

    class Meta:
        model = Product
        fields = [
            'name', 'barcode', 'sku', 'category', 'brand', 'supplier',
            'purchase_price', 'selling_price', 'tax_rate', 'discount_rate',
            'stock_quantity', 'min_stock_level', 'description', 'image', 'status'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'barcode': forms.TextInput(attrs={'class': 'form-control'}),
            'sku': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'brand': forms.Select(attrs={'class': 'form-select'}),
            'supplier': forms.Select(attrs={'class': 'form-select'}),
            'purchase_price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'selling_price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'required': True}),
            'tax_rate': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'discount_rate': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'stock_quantity': forms.NumberInput(attrs={'class': 'form-control', 'required': True}),
            'min_stock_level': forms.NumberInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'status': forms.CheckboxInput(attrs={'class': 'form-check-input', 'checked': True}),
        }
