from django import forms
from .models import Transaction, Account, Subscription


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


class SubscriptionForm(forms.ModelForm):
    class Meta:
        model = Subscription
        fields = [
            'name',
            'purpose',
            'amount',
            'currency',
            'account',
            'project',
            'next_payment_date',
            'frequency',
            'status',
            'reminder_days_before',
            'notes',
        ]
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Spotify Premium'
            }),
            'purpose': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Why do you keep this subscription?'
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
            'account': forms.Select(attrs={
                'class': 'form-select'
            }),
            'project': forms.Select(attrs={
                'class': 'form-select'
            }),
            'next_payment_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'frequency': forms.Select(attrs={
                'class': 'form-select'
            }),
            'status': forms.Select(attrs={
                'class': 'form-select'
            }),
            'reminder_days_before': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0,
                'step': 1,
                'placeholder': 'Days before next payment'
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Add any extra details, renewal reminders, promo codes, etc.'
            }),
        }
        labels = {
            'name': 'Subscription Name',
            'purpose': 'Purpose (Optional)',
            'amount': 'Amount',
            'currency': 'Currency',
            'account': 'Account (Optional)',
            'project': 'Project (Optional)',
            'next_payment_date': 'Next Payment Date',
            'frequency': 'Frequency',
            'status': 'Status',
            'reminder_days_before': 'Reminder (days before)',
            'notes': 'Notes (Optional)',
        }
