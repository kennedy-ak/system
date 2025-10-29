from django import forms
from .models import Transaction


class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['project', 'amount', 'currency', 't_type', 'description']
        widgets = {
            'project': forms.Select(attrs={
                'class': 'form-select'
            }),
            'amount': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '0.00',
                'step': '0.01'
            }),
            'currency': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'USD'
            }),
            't_type': forms.Select(attrs={
                'class': 'form-select'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Add a description...',
                'rows': 4
            }),
        }
        labels = {
            'project': 'Project (Optional)',
            'amount': 'Amount',
            'currency': 'Currency',
            't_type': 'Transaction Type',
            'description': 'Description',
        }
