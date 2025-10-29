from django.db import models
from django.conf import settings
from django.urls import reverse


class Transaction(models.Model):
    TRANSACTION_TYPES = (("income", "Income"), ("expense", "Expense"))

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    project = models.ForeignKey('projects.Project', on_delete=models.SET_NULL, null=True, blank=True, related_name='transactions')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=10, default='USD')
    t_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    description = models.TextField(blank=True)
    date = models.DateField(auto_now_add=True)  # Automatically set to today when created
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.t_type} {self.amount} by {self.user.username} on {self.date}"
        
    def get_absolute_url(self):
        return reverse('finance:transaction_list')