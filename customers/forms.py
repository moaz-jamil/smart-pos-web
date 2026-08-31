from django import forms
from customers.models import Customer

class CustomerForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['reward_points'].required = False
        self.fields['reward_points'].initial = 0
        self.fields['wallet_balance'].required = False
        self.fields['wallet_balance'].initial = 0.00
        self.fields['outstanding_balance'].required = False
        self.fields['outstanding_balance'].initial = 0.00
        self.fields['email'].required = False
        self.fields['address'].required = False
        self.fields['status'].required = False

    class Meta:
        model = Customer
        fields = ['name', 'phone', 'email', 'address', 'reward_points', 'wallet_balance', 'outstanding_balance', 'status']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'reward_points': forms.NumberInput(attrs={'class': 'form-control'}),
            'wallet_balance': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'outstanding_balance': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'status': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
