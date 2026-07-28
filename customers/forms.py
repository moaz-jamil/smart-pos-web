from django import forms
from customers.models import Customer

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'phone', 'email', 'address', 'reward_points', 'wallet_balance', 'outstanding_balance', 'status']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'reward_points': forms.NumberInput(attrs={'class': 'form-control'}),
            'wallet_balance': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'outstanding_balance': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'status': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
