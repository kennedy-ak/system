from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from decimal import Decimal
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

    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        if amount is not None and amount <= 0:
            raise ValidationError("Amount must be greater than zero.")
        return amount


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

    def clean_initial_balance(self):
        balance = self.cleaned_data.get('initial_balance')
        if balance is not None and balance < 0:
            raise ValidationError("Initial balance cannot be negative.")
        return balance


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
            'enable_reminders',
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
            'enable_reminders': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
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
            'enable_reminders': 'Enable SMS Reminders',
            'notes': 'Notes (Optional)',
        }

    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        if amount is not None and amount <= 0:
            raise ValidationError("Amount must be greater than zero.")
        return amount

    def clean_next_payment_date(self):
        date = self.cleaned_data.get('next_payment_date')
        if date and date < timezone.now().date():
            raise ValidationError("Next payment date cannot be in the past.")
        return date

    def clean_reminder_days_before(self):
        days = self.cleaned_data.get('reminder_days_before')
        if days is not None and days < 0:
            raise ValidationError("Reminder days must be positive.")
        if days is not None and days > 365:
            raise ValidationError("Reminder days cannot exceed 365.")
        return days
