from django import forms
from .models import Transaction, Account


class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['account', 'project', 'amount', 'currency', 't_type', 'category', 'description']
        widgets = {
            'account': forms.Select(attrs={
                'class': 'form-select'
            }),
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
                'placeholder': 'GHS'
            }),
            't_type': forms.Select(attrs={
                'class': 'form-select'
            }),
            'category': forms.Select(attrs={
                'class': 'form-select'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Add a description...',
                'rows': 4
            }),
        }
        labels = {
            'account': 'Account',
            'project': 'Project (Optional)',
            'amount': 'Amount',
            'currency': 'Currency',
            't_type': 'Transaction Type',
            'category': 'Category',
            'description': 'Description',
        }


class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['name', 'account_type', 'currency', 'initial_balance', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Chase Checking'
            }),
            'account_type': forms.Select(attrs={
                'class': 'form-select'
            }),
            'currency': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'GHS'
            }),
            'initial_balance': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '0.00',
                'step': '0.01'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }
        labels = {
            'name': 'Account Name',
            'account_type': 'Account Type',
            'currency': 'Currency',
            'initial_balance': 'Initial Balance',
            'is_active': 'Active',
        }
