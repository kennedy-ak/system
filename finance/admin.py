from django.contrib import admin
from .models import Transaction, Account, Subscription


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ['name', 'account_type', 'user', 'currency', 'initial_balance', 'is_active', 'created_at']
    list_filter = ['account_type', 'is_active', 'currency', 'user']
    search_fields = ['name', 'user__username']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['user', 'account', 'project', 't_type', 'category', 'amount', 'currency', 'date']
    list_filter = ['t_type', 'category', 'currency', 'date', 'user', 'account']
    search_fields = ['description', 'user__username', 'project__title', 'category']
    date_hierarchy = 'date'
    readonly_fields = ['date', 'created_at']


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'user',
        'account',
        'project',
        'amount',
        'currency',
        'frequency',
        'status',
        'next_payment_date',
        'updated_at',
    ]
    list_filter = ['frequency', 'status', 'currency', 'next_payment_date', 'user', 'account']
    search_fields = ['name', 'purpose', 'notes', 'user__username', 'project__title', 'account__name']
    ordering = ['next_payment_date', 'name']
    readonly_fields = ['created_at', 'updated_at']
