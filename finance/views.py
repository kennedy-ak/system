from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic

from .models import Transaction
from .forms import TransactionForm


class TransactionListView(LoginRequiredMixin, generic.ListView):
    model = Transaction
    template_name = 'finance/transaction_list.html'


class TransactionCreateView(LoginRequiredMixin, generic.CreateView):
    model = Transaction
    form_class = TransactionForm
    template_name = 'finance/transaction_form.html'

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        # Only show projects owned by the current user
        form.fields['project'].queryset = self.request.user.projects.all()
        return form

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class TransactionUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Transaction
    form_class = TransactionForm
    template_name = 'finance/transaction_form.html'

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        # Only show projects owned by the current user
        form.fields['project'].queryset = self.request.user.projects.all()
        return form


class TransactionDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Transaction
    success_url = reverse_lazy('finance:transaction_list')
    template_name = 'finance/transaction_confirm_delete.html'
from django.shortcuts import render

# Create your views here.
