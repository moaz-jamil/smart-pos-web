from django import forms
from suppliers.models import Supplier

class SupplierForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['outstanding_balance'].required = False
        self.fields['outstanding_balance'].initial = 0.00
        self.fields['contact_name'].required = False
        self.fields['email'].required = False
        self.fields['address'].required = False
        self.fields['status'].required = False

    class Meta:
        model = Supplier
        fields = ['company_name', 'contact_name', 'phone', 'email', 'address', 'outstanding_balance', 'status']
        widgets = {
            'company_name': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'contact_name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'outstanding_balance': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'status': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
