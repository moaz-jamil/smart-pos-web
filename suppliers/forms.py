from django import forms
from suppliers.models import Supplier

class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = ['company_name', 'contact_name', 'phone', 'email', 'address', 'outstanding_balance', 'status']
        widgets = {
            'company_name': forms.TextInput(attrs={'class': 'form-control'}),
            'contact_name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'outstanding_balance': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'status': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
