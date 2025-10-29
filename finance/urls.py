from django.urls import path
from .views import (
    TransactionListView,
    TransactionCreateView,
    TransactionUpdateView,
    TransactionDeleteView,
)

app_name = 'finance'

urlpatterns = [
    path('', TransactionListView.as_view(), name='transaction_list'),
    path('create/', TransactionCreateView.as_view(), name='transaction_create'),
    path('<int:pk>/edit/', TransactionUpdateView.as_view(), name='transaction_edit'),
    path('<int:pk>/delete/', TransactionDeleteView.as_view(), name='transaction_delete'),
]
