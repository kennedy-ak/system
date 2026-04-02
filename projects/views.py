from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from django.db.models import Q
from django.contrib import messages

from myhub.mixins import UserIsOwnerMixin, SuccessMessageMixin
from .models import Project
from .forms import ProjectForm


class ProjectListView(LoginRequiredMixin, generic.ListView):
    model = Project
    template_name = 'projects/project_list.html'
    paginate_by = 10

    def get_queryset(self):
        queryset = Project.objects.filter(owner=self.request.user)
        search_query = self.request.GET.get('search', '')
        status_filter = self.request.GET.get('status', '')

        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) |
                Q(description__icontains=search_query)
            )

        if status_filter:
            queryset = queryset.filter(status=status_filter)

        return queryset.order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('search', '')
        context['status_filter'] = self.request.GET.get('status', '')
        return context


class ProjectCreateView(LoginRequiredMixin, SuccessMessageMixin, generic.CreateView):
    model = Project
    form_class = ProjectForm
    template_name = 'projects/project_form.html'
    success_message = "Project created successfully."

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class ProjectDetailView(LoginRequiredMixin, UserIsOwnerMixin, generic.DetailView):
    model = Project
    template_name = 'projects/project_detail.html'

    def get_queryset(self):
        return Project.objects.select_related('owner').prefetch_related('transactions', 'tasks')


class ProjectUpdateView(LoginRequiredMixin, UserIsOwnerMixin, SuccessMessageMixin, generic.UpdateView):
    model = Project
    form_class = ProjectForm
    template_name = 'projects/project_form.html'
    success_message = "Project updated successfully."


class ProjectDeleteView(LoginRequiredMixin, UserIsOwnerMixin, SuccessMessageMixin, generic.DeleteView):
    model = Project
    success_url = reverse_lazy('projects:project_list')
    template_name = 'projects/project_confirm_delete.html'
    success_message = "Project deleted successfully."
