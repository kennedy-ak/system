from decimal import Decimal

from django.db import models
from django.conf import settings
from django.urls import reverse


class Account(models.Model):
    ACCOUNT_TYPES = (
        ('checking', 'Checking'),
        ('savings', 'Savings'),
        ('credit_card', 'Credit Card'),
        ('cash', 'Cash'),
        ('investment', 'Investment'),
        ('other', 'Other'),
    )

    name = models.CharField(max_length=200)
    account_type = models.CharField(max_length=20, choices=ACCOUNT_TYPES, default='checking')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='accounts')
    currency = models.CharField(max_length=10, default='GHS')
    initial_balance = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'), help_text="Starting balance when you began tracking this account")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.get_account_type_display()})"

    def get_absolute_url(self):
        return reverse('finance:account_detail', kwargs={'pk': self.pk})

    def current_balance(self):
        """Calculate current balance based on initial balance + all transactions"""
        total_income = self.transactions.filter(t_type='income').aggregate(
            total=models.Sum('amount')
        )['total'] or 0
        total_expense = self.transactions.filter(t_type='expense').aggregate(
            total=models.Sum('amount')
        )['total'] or 0
        return self.initial_balance + total_income - total_expense


class Transaction(models.Model):
    TRANSACTION_TYPES = (("income", "Income"), ("expense", "Expense"))

    INCOME_CATEGORIES = (
        ('salary', 'Salary'),
        ('freelance', 'Freelance'),
        ('investment', 'Investment'),
        ('gift', 'Gift'),
        ('refund', 'Refund'),
        ('other_income', 'Other Income'),
    )

    EXPENSE_CATEGORIES = (
        ('food', 'Food & Dining'),
        ('transport', 'Transportation'),
        ('entertainment', 'Entertainment'),
        ('bills', 'Bills & Utilities'),
        ('shopping', 'Shopping'),
        ('health', 'Health & Medical'),
        ('education', 'Education'),
        ('travel', 'Travel'),
        ('groceries', 'Groceries'),
        ('rent', 'Rent/Mortgage'),
        ('insurance', 'Insurance'),
        ('other_expense', 'Other Expense'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='transactions', null=True, blank=True)
    project = models.ForeignKey('projects.Project', on_delete=models.SET_NULL, null=True, blank=True, related_name='transactions')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=10, default='GHS')
    t_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    category = models.CharField(max_length=30, blank=True)
    description = models.TextField(blank=True)
    date = models.DateField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date', '-created_at']

    def __str__(self):
        return f"{self.t_type} {self.amount} - {self.category or 'Uncategorized'} on {self.date}"

    def get_absolute_url(self):
        return reverse('finance:transaction_list')

    @classmethod
    def get_category_choices(cls, transaction_type):
        """Get category choices based on transaction type"""
        if transaction_type == 'income':
            return cls.INCOME_CATEGORIES
        else:
            return cls.EXPENSE_CATEGORIES


class Subscription(models.Model):
    FREQUENCY_CHOICES = (
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('quarterly', 'Quarterly'),
        ('yearly', 'Yearly'),
        ('custom', 'Custom'),
    )

    STATUS_CHOICES = (
        ('active', 'Active'),
        ('paused', 'Paused'),
        ('canceled', 'Canceled'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='subscriptions')
    account = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True, blank=True, related_name='subscriptions')
    project = models.ForeignKey('projects.Project', on_delete=models.SET_NULL, null=True, blank=True, related_name='subscriptions')
    name = models.CharField(max_length=255)
    purpose = models.TextField(blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=10, default='GHS')
    next_payment_date = models.DateField()
    frequency = models.CharField(max_length=20, choices=FREQUENCY_CHOICES, default='monthly')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    reminder_days_before = models.PositiveIntegerField(default=2, help_text="Days before next payment to send reminder SMS")
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['next_payment_date', 'name']

    def __str__(self):
        return f"{self.name} - {self.amount} {self.currency}"

    def get_absolute_url(self):
        return reverse('finance:subscription_detail', kwargs={'pk': self.pk})