from django.urls import path
from .views import (
    TransactionListView,
    TransactionCreateView,
    TransactionUpdateView,
    TransactionDeleteView,
    AccountListView,
    AccountDetailView,
    AccountCreateView,
    AccountUpdateView,
    AccountDeleteView,
    SubscriptionListView,
    SubscriptionDetailView,
    SubscriptionCreateView,
    SubscriptionUpdateView,
    SubscriptionDeleteView,
)

app_name = 'finance'

urlpatterns = [
    # Transaction URLs
    path('', TransactionListView.as_view(), name='transaction_list'),
    path('create/', TransactionCreateView.as_view(), name='transaction_create'),
    path('<int:pk>/edit/', TransactionUpdateView.as_view(), name='transaction_edit'),
    path('<int:pk>/delete/', TransactionDeleteView.as_view(), name='transaction_delete'),

    # Account URLs
    path('accounts/', AccountListView.as_view(), name='account_list'),
    path('accounts/create/', AccountCreateView.as_view(), name='account_create'),
    path('accounts/<int:pk>/', AccountDetailView.as_view(), name='account_detail'),
    path('accounts/<int:pk>/edit/', AccountUpdateView.as_view(), name='account_update'),
    path('accounts/<int:pk>/delete/', AccountDeleteView.as_view(), name='account_delete'),

    # Subscription URLs
    path('subscriptions/', SubscriptionListView.as_view(), name='subscription_list'),
    path('subscriptions/create/', SubscriptionCreateView.as_view(), name='subscription_create'),
    path('subscriptions/<int:pk>/', SubscriptionDetailView.as_view(), name='subscription_detail'),
    path('subscriptions/<int:pk>/edit/', SubscriptionUpdateView.as_view(), name='subscription_update'),
    path('subscriptions/<int:pk>/delete/', SubscriptionDeleteView.as_view(), name='subscription_delete'),
]
