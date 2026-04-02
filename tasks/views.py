from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from django.db.models import Q
from django.contrib import messages

from myhub.mixins import UserIsOwnerMixin, SuccessMessageMixin
from .models import Task
from .forms import TaskForm


class TaskListView(LoginRequiredMixin, generic.ListView):
    model = Task
    template_name = 'tasks/task_list.html'
    paginate_by = 20

    def get_queryset(self):
        queryset = Task.objects.filter(user=self.request.user).select_related('project', 'user')
        search_query = self.request.GET.get('search', '')
        status_filter = self.request.GET.get('status', '')
        priority_filter = self.request.GET.get('priority', '')
        project_filter = self.request.GET.get('project', '')

        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) |
                Q(description__icontains=search_query)
            )

        if status_filter:
            queryset = queryset.filter(status=status_filter)

        if priority_filter:
            queryset = queryset.filter(priority=priority_filter)

        if project_filter:
            queryset = queryset.filter(project_id=project_filter)

        return queryset.order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('search', '')
        context['status_filter'] = self.request.GET.get('status', '')
        context['priority_filter'] = self.request.GET.get('priority', '')
        context['project_filter'] = self.request.GET.get('project', '')
        context['user_projects'] = self.request.user.projects.all()
        return context


class TaskCreateView(LoginRequiredMixin, SuccessMessageMixin, generic.CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/task_form.html'
    success_message = "Task created successfully."

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        # Only show projects owned by the current user
        form.fields['project'].queryset = self.request.user.projects.all()
        return form

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class TaskDetailView(LoginRequiredMixin, UserIsOwnerMixin, generic.DetailView):
    model = Task
    template_name = 'tasks/task_detail.html'


class TaskUpdateView(LoginRequiredMixin, UserIsOwnerMixin, SuccessMessageMixin, generic.UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/task_form.html'
    success_message = "Task updated successfully."

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        # Only show projects owned by the current user
        form.fields['project'].queryset = self.request.user.projects.all()
        return form


class TaskDeleteView(LoginRequiredMixin, UserIsOwnerMixin, SuccessMessageMixin, generic.DeleteView):
    model = Task
    success_url = reverse_lazy('tasks:task_list')
    template_name = 'tasks/task_confirm_delete.html'
    success_message = "Task deleted successfully."
