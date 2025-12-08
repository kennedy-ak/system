from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views import generic
from django.db.models import Q, Sum
from django import forms

from .models import Transaction, Account
from .forms import TransactionForm, AccountForm


class TransactionListView(LoginRequiredMixin, generic.ListView):
    model = Transaction
    template_name = 'finance/transaction_list.html'
    paginate_by = 20

    def get_queryset(self):
        queryset = Transaction.objects.filter(user=self.request.user).select_related('project', 'user', 'account')
        search_query = self.request.GET.get('search', '')
        type_filter = self.request.GET.get('type', '')
        project_filter = self.request.GET.get('project', '')
        account_filter = self.request.GET.get('account', '')
        category_filter = self.request.GET.get('category', '')

        if search_query:
            queryset = queryset.filter(
                Q(description__icontains=search_query) |
                Q(amount__icontains=search_query) |
                Q(category__icontains=search_query)
            )

        if type_filter:
            queryset = queryset.filter(t_type=type_filter)

        if project_filter:
            queryset = queryset.filter(project_id=project_filter)

        if account_filter:
            queryset = queryset.filter(account_id=account_filter)

        if category_filter:
            queryset = queryset.filter(category=category_filter)

        return queryset.order_by('-date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('search', '')
        context['type_filter'] = self.request.GET.get('type', '')
        context['project_filter'] = self.request.GET.get('project', '')
        context['account_filter'] = self.request.GET.get('account', '')
        context['category_filter'] = self.request.GET.get('category', '')
        context['user_projects'] = self.request.user.projects.all()
        context['user_accounts'] = self.request.user.accounts.filter(is_active=True)
        return context


class TransactionCreateView(LoginRequiredMixin, generic.CreateView):
    model = Transaction
    form_class = TransactionForm
    template_name = 'finance/transaction_form.html'

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        # Only show projects and accounts owned by the current user
        form.fields['project'].queryset = self.request.user.projects.all()
        form.fields['account'].queryset = self.request.user.accounts.filter(is_active=True)

        # Update category choices based on transaction type if form has data
        if self.request.POST:
            t_type = self.request.POST.get('t_type', '')
            if t_type:
                choices = Transaction.get_category_choices(t_type)
                form.fields['category'].widget = forms.Select(attrs={'class': 'form-select'}, choices=[('', '---------')] + list(choices))

        return form

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class TransactionUpdateView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    model = Transaction
    form_class = TransactionForm
    template_name = 'finance/transaction_form.html'

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        # Only show projects and accounts owned by the current user
        form.fields['project'].queryset = self.request.user.projects.all()
        form.fields['account'].queryset = self.request.user.accounts.filter(is_active=True)

        # Update category choices based on transaction type
        if self.request.POST:
            t_type = self.request.POST.get('t_type', '')
        else:
            t_type = self.object.t_type

        if t_type:
            choices = Transaction.get_category_choices(t_type)
            form.fields['category'].widget = forms.Select(attrs={'class': 'form-select'}, choices=[('', '---------')] + list(choices))

        return form

    def test_func(self):
        transaction = self.get_object()
        return transaction.user == self.request.user


class TransactionDeleteView(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    model = Transaction
    success_url = reverse_lazy('finance:transaction_list')
    template_name = 'finance/transaction_confirm_delete.html'

    def test_func(self):
        transaction = self.get_object()
        return transaction.user == self.request.user


# Account Views

class AccountListView(LoginRequiredMixin, generic.ListView):
    model = Account
    template_name = 'finance/account_list.html'
    context_object_name = 'accounts'

    def get_queryset(self):
        return Account.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        accounts = context['accounts']
        total_balance = sum(acc.current_balance() for acc in accounts)
        context['total_balance'] = total_balance
        return context


class AccountDetailView(LoginRequiredMixin, UserPassesTestMixin, generic.DetailView):
    model = Account
    template_name = 'finance/account_detail.html'

    def get_queryset(self):
        return Account.objects.prefetch_related('transactions')

    def test_func(self):
        account = self.get_object()
        return account.user == self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        account = self.object
        recent_transactions = account.transactions.all()[:10]
        context['recent_transactions'] = recent_transactions
        context['current_balance'] = account.current_balance()
        return context


class AccountCreateView(LoginRequiredMixin, generic.CreateView):
    model = Account
    form_class = AccountForm
    template_name = 'finance/account_form.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class AccountUpdateView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    model = Account
    form_class = AccountForm
    template_name = 'finance/account_form.html'

    def test_func(self):
        account = self.get_object()
        return account.user == self.request.user


class AccountDeleteView(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    model = Account
    success_url = reverse_lazy('finance:account_list')
    template_name = 'finance/account_confirm_delete.html'

    def test_func(self):
        account = self.get_object()
        return account.user == self.request.user
