from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from django.db.models import Q
from django.contrib import messages

from myhub.mixins import UserIsOwnerMixin, SuccessMessageMixin
from .models import WorkLog
from .forms import WorkLogForm


class WorkLogListView(LoginRequiredMixin, generic.ListView):
    model = WorkLog
    template_name = 'worklogs/worklog_list.html'
    paginate_by = 10

    def get_queryset(self):
        queryset = WorkLog.objects.filter(user=self.request.user).select_related('project', 'task')
        search_query = self.request.GET.get('search', '')
        status_filter = self.request.GET.get('status', '')

        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) |
                Q(description__icontains=search_query) |
                Q(notes__icontains=search_query)
            )

        if status_filter:
            queryset = queryset.filter(status=status_filter)

        return queryset.order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('search', '')
        context['status_filter'] = self.request.GET.get('status', '')
        return context


class WorkLogDetailView(LoginRequiredMixin, UserIsOwnerMixin, generic.DetailView):
    model = WorkLog
    template_name = 'worklogs/worklog_detail.html'

    def get_queryset(self):
        return WorkLog.objects.select_related('user', 'project', 'task')


class WorkLogCreateView(LoginRequiredMixin, SuccessMessageMixin, generic.CreateView):
    model = WorkLog
    form_class = WorkLogForm
    template_name = 'worklogs/worklog_form.html'
    success_message = "Work log created successfully."

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class WorkLogUpdateView(LoginRequiredMixin, UserIsOwnerMixin, SuccessMessageMixin, generic.UpdateView):
    model = WorkLog
    form_class = WorkLogForm
    template_name = 'worklogs/worklog_form.html'
    success_message = "Work log updated successfully."

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class WorkLogDeleteView(LoginRequiredMixin, UserIsOwnerMixin, SuccessMessageMixin, generic.DeleteView):
    model = WorkLog
    success_url = reverse_lazy('worklogs:worklog_list')
    template_name = 'worklogs/worklog_confirm_delete.html'
    success_message = "Work log deleted successfully."
